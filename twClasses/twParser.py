from twClasses.twFakeBee import XBee
from math import ceil
import struct


class Parser:
	def __init__(self):
		self._packet_size = 256
		self._message_id_bytes = 4
		self._packet_id_bytes = 2
		self._dtype_bytes = 1
		self._sensor_id_bytes = 2
		self._message_id_count = 0
		self._packet_id_count = 0
		self._id = "B1"
		self._start_flag = "<"
		self._end_flag = ">"

	@staticmethod
	def chunkstring(string: bytes, length: int) -> iter:
		return (string[0 + i:length + i] for i in range(0, len(string), length))

	@staticmethod
	def number_of_packets(packet: bytes, length: int) -> bytes:
		value = ceil(len(packet) / length)
		return Parser.ushort_to_bytes(value)

	@staticmethod
	def ushort_to_bytes(number: int) -> bytes:
		return struct.pack(">H", number)

	@staticmethod
	def uint_to_bytes(number: int) -> bytes:
		return struct.pack(">I", number)

	@staticmethod
	def double_to_bytes(number: float) -> bytes:
		return struct.pack(">d", number)

	@staticmethod
	def string_to_bytes(string: str) -> bytes:
		return string.encode()

	@staticmethod
	def char_to_bytes(char: str) -> bytes:
		return char.encode()

	@staticmethod
	def long_long_to_bytes(long: int) -> bytes:
		return struct.pack(">q", long)

	@staticmethod
	def bytes_to_ushort(number: bytes) -> int:
		return struct.unpack(">H", number)[0]

	@staticmethod
	def bytes_to_uint(number_bytes: bytes) -> int:
		return struct.unpack(">I", number_bytes)[0]

	@staticmethod
	def bytes_to_double(number: bytes) -> float:
		return struct.unpack(">d", number)[0]

	@staticmethod
	def bytes_to_string(string: bytes) -> str:
		return string.decode()

	@staticmethod
	def bytes_to_char(char: bytes) -> str:
		return char.decode()

	@staticmethod
	def bytes_to_long_long(long: bytes) -> int:
		return struct.unpack(">q", long)[0]

	@staticmethod
	def convert_value_from_bytes(value: bytes, data_type: str):
		if data_type == "I":
			return Parser.bytes_to_long_long(value)
		elif data_type == "d":
			return Parser.bytes_to_double(value)
		else:
			return Parser.bytes_to_string(value)

	def _next_message_id(self) -> int:
		self._message_id_count += 1
		return self._message_id_count

	def _next_packet_id(self) -> int:
		self._packet_id_count += 1
		return self._packet_id_count

	def prepare_command(self, command: str) -> list:
		sending_packets = []
		data_set_id = self._next_message_id()
		sensor_id = Parser.string_to_bytes(self._id)
		dtype = Parser.char_to_bytes("s")
		data_set_id_bytes = Parser.uint_to_bytes(data_set_id)
		content_count = self._packet_size - self._message_id_bytes - self._packet_id_bytes*2 - self._sensor_id_bytes - \
						self._dtype_bytes - len(self._start_flag) - len(self._end_flag)
		content = Parser.string_to_bytes(command)
		start_flag = Parser.char_to_bytes(self._start_flag)
		end_flag = Parser.char_to_bytes(self._end_flag)
		packet_number_bytes = Parser.number_of_packets(content, content_count)
		for packet in Parser.chunkstring(content, content_count):
			packet_id = self._next_packet_id()
			packet_id_bytes = Parser.ushort_to_bytes(packet_id)
			ready_packet = start_flag + data_set_id_bytes + packet_id_bytes + packet_number_bytes + dtype + sensor_id + \
						   packet + end_flag
			sending_packets.append(ready_packet)
		self._packet_id_count = 0
		return sending_packets

	def parse_message(self, message: bytes) -> dict:
		message = message[1:-1]
		message_number_bytes = message[0:4]
		packet_total_bytes = message[6:8]
		dtype_bytes = message[8:9]
		message_type_bytes = message[9:11]
		# TODO: Build special case for images
		message_json = {
			"message_number": Parser.bytes_to_uint(message_number_bytes),
			"value_type": Parser.bytes_to_string(message_type_bytes),
			"total_packets": Parser.bytes_to_ushort(packet_total_bytes),
			"data_type": Parser.bytes_to_char(dtype_bytes)
		}
		return message_json

	def parse_packet(self, message: bytes) -> dict:
		message = message[1:-1]
		packet_number_bytes = message[4:6]
		content = message[11:]
		packet_json = {
			"packet_number": Parser.bytes_to_ushort(packet_number_bytes),
			"content": content
		}
		return packet_json
