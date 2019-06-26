from twClasses.twFakeBee import XBee


class Parser:
	def __init__(self):
		self._packet_size = 256
		self._start_flag = "<"
		self._end_flag = ">"
		self._message_id_bytes = 4
		self._packet_id_bytes = 3
		self._message_id_count = 0
		self._packet_id_count = 0
		self._transceiverDevice = XBee()

	@staticmethod
	def chunkstring(string: str, length: int) -> iter:
		return (string[0 + i:length + i] for i in range(0, len(string), length))

	@staticmethod
	def int_to_bytes(number: int, length):
		return number.to_bytes(length=length, byteorder="big")

	def _prepare_for_sending(self, packet: bytes) -> bytes:
		return self._start_flag.encode() + packet + self._end_flag.encode()

	def _next_message_id(self) -> int:
		self._message_id_count += 1
		return self._message_id_count

	def _next_packet_id(self) -> int:
		self._packet_id_count += 1
		return self._packet_id_count

	def send_command(self, command: str) -> list:
		sending_packets = []
		data_set_id = self._next_message_id()
		data_set_id_bytes = Parser.int_to_bytes(data_set_id, self._message_id_bytes)
		content_count = self._packet_size - len(self._start_flag) - len(self._end_flag) - self._message_id_bytes\
						- self._packet_id_bytes
		for packet in Parser.chunkstring(command, content_count):
			packet_id = self._next_packet_id()
			packet_id_bytes = Parser.int_to_bytes(packet_id, self._packet_id_bytes)
			ready_packet = self._prepare_for_sending(data_set_id_bytes + packet_id_bytes + packet.encode())
			self._transceiverDevice.write(ready_packet)
			sending_packets.append({
				"packet_number": packet_id,
				"content": packet,
			})
		self._packet_id_count = 0
		return sending_packets
