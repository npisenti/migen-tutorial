/* Machine-generated using Migen */
module top(
	input ttl,
	input ttl_1,
	output ttl_2,
	output ttl_3,
	output ttl_4,
	output ttl_5,
	input clk50
);

wire d;
wire en;
reg r0 = 1'd0;
reg r1 = 1'd1;
wire r2;
wire r3;
reg wait_1 = 1'd0;
wire done;
reg [3:0] count = 4'd10;
reg xilinxisetoolchain_state = 1'd0;
reg xilinxisetoolchain_next_state = 1'd0;
wire sys_clk;
wire sys_rst;
wire por_clk;
reg xilinxisetoolchain_int_rst = 1'd1;

// synthesis translate_off
reg dummy_s;
initial dummy_s <= 1'd0;
// synthesis translate_on
assign r2 = r0;
assign r3 = r1;
assign en = ttl;
assign d = ttl_1;
assign ttl_2 = r0;
assign ttl_3 = r1;
assign ttl_4 = r2;
assign ttl_5 = r3;

// synthesis translate_off
reg dummy_d;
// synthesis translate_on
always @(*) begin
	r1 <= 1'd1;
	xilinxisetoolchain_next_state <= 1'd0;
	r0 <= 1'd0;
	wait_1 <= 1'd0;
	xilinxisetoolchain_next_state <= xilinxisetoolchain_state;
	case (xilinxisetoolchain_state)
		1'd1: begin
			if (en) begin
				r0 <= d;
				r1 <= (~d);
			end else begin
				xilinxisetoolchain_next_state <= 1'd0;
			end
		end
		default: begin
			if (en) begin
				wait_1 <= 1'd1;
			end else begin
				wait_1 <= 1'd0;
			end
			if (done) begin
				xilinxisetoolchain_next_state <= 1'd1;
			end
		end
	endcase
// synthesis translate_off
	dummy_d <= dummy_s;
// synthesis translate_on
end
assign done = (count == 1'd0);
assign sys_clk = clk50;
assign por_clk = clk50;
assign sys_rst = xilinxisetoolchain_int_rst;

always @(posedge por_clk) begin
	xilinxisetoolchain_int_rst <= 1'd0;
end

always @(posedge sys_clk) begin
	if (sys_rst) begin
		count <= 4'd10;
		xilinxisetoolchain_state <= 1'd0;
	end else begin
		xilinxisetoolchain_state <= xilinxisetoolchain_next_state;
		if (wait_1) begin
			if ((~done)) begin
				count <= (count - 1'd1);
			end
		end else begin
			count <= 4'd10;
		end
	end
end

endmodule
