from digi.xbee.devices import XBeeDevice
from digi.xbee.devices import RemoteXBeeDevice
from digi.xbee.reader import XBee64BitAddress


class XBee:
	def __init__(self, path_to_device, baud_rate=9600):
		self._device = XBeeDevice(path_to_device, baud_rate)
		self._device.open()

	def write(self, message, address):
		if len(message) > 256:
			raise UserWarning("Message to large. Will be truncated")
			message = message[0:256]
		remote_device = RemoteXBeeDevice(self._device, XBee64BitAddress.from_hex_string(address))
		self._device.send_data_async(remote_device, message)
		return True

	def set_callback(self, callback_method):
		self._device.add_data_received_callback(callback_method)
		return True
