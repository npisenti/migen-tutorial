from migen import *
from migen.genlib.fsm import FSM
from migen.genlib.misc import WaitTimer

from coolrunner import coolrunner
from migen.build.generic_platform import *

class HBridgeDriver(Module):
    def __init__(self, delay):

        # inputs
        self.d = Signal()  # coil direction
        self.en = Signal() # enable switching of direction

        # outputs
        # signals driving relay on/off; will need to be wired to physical pin
        # in platform definition/top-level build
        self.r0 = Signal(reset=0)
        self.r1 = Signal(reset=1)
        self.r2 = Signal()
        self.r3 = Signal()

        self.delay = delay # store attribute for testbench...?

        # declaring these here is a pattern for doing, eg, the following in platform build:
        #    top.comb += [platform.request("ttl").eq(o) for o in top.outputs]
        # (where `top` is an instance of HBridgeDriver)
        self.inputs = [self.en, self.d]
        self.outputs = [self.r0, self.r1, self.r2, self.r3]

        # # #

        # this syntax exposes these submodules as self.fsm, self.timer as well
        self.submodules.fsm = fsm = FSM(reset_state="LOCKOUT")
        self.submodules.timer = timer = WaitTimer(delay)

        # state machine
        # "LOCKOUT" -> do not allow coil direction change. Exit this state
        #              conditioned on zero current, plus some "delay" for ringdown
        # "ENABLE" -> do allow coil direction to swap
        fsm.act("LOCKOUT",
            If(self.en,
                timer.wait.eq(1)
            ).Else(timer.wait.eq(0)),
            If(timer.done, NextState("ENABLE"))
        )

        ## break before make needs to be implemented
        fsm.act("ENABLE",
            If(self.en,
                self.r0.eq(self.d),
                self.r1.eq(~self.d)
            ).Else(NextState("LOCKOUT"))
        )

        # will need to check polarity here for relay connections to
        # get proper h-bridge behavior...
        self.comb += [self.r2.eq(self.r0), self.r3.eq(self.r1)]


_pipistrello_io = [
    ("ttl", 0, Pins("BANK1:11"), IOStandard("LVTTL")),
    ("ttl", 1, Pins("BANK1:10"), IOStandard("LVTTL")),
    ("ttl", 2, Pins("BANK1:9"), IOStandard("LVTTL")),
    ("ttl", 3, Pins("BANK1:8"), IOStandard("LVTTL")),
    ("ttl", 4, Pins("BANK1:7"), IOStandard("LVTTL")),
    ("ttl", 5, Pins("BANK1:5"), IOStandard("LVTTL")),
    ("ttl", 6, Pins("BANK1:4"), IOStandard("LVTTL"))
]

def build_platform(delay=10000000000):
    platform = coolrunner.Platform()

    # must `add_extension` to be able to request IO
    platform.add_extension(_pipistrello_io)

    top = HBridgeDriver(delay)

    # drive direction, enable signals from first two TTL
    # alternatively, could do platform.request("ttl", 0), ... to get explicit
    top.comb += [
        top.en.eq(platform.request("ttl")),
        top.d.eq(platform.request("ttl"))
    ]

    # drive output pins
    # (general) QUESTION: do you have to explicitly declare in vs out? or is it inferred
    # from reg vs wire...?
    top.comb += [platform.request("ttl").eq(o) for o in top.outputs]

    platform.build(top, build_dir="bridge_build", build_name="hbridge_top")
    platform.run(build_dir="bridge_build", build_name="hbridge_top")

if __name__ == "__main__":
    build_platform()
