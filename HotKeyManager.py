from time import time
from enum import IntEnum
from pynput.keyboard import Listener, Key, KeyCode


class HotKeyType(IntEnum):
    # single key
    SINGLE = 1
    # multiple keys
    MULTIPLE = 2


class HotKey:
    def __init__(self, trigger, key_type, keys, count=2, interval=0.5):
        """
        :param trigger: Function called when hot key is triggered.
        :param HotKeyType key_type: type of hot key.
        :param list keys: Key list.
        :param int count: The press times of hot key. Only for single type hot key.
        :param float interval: The interval time between presses, unit: second. Only for single type hot key.
        """
        if callable(trigger):
            self.__trigger = trigger
        else:
            raise TypeError('Wrong type, "trigger" must be a function.')
        if isinstance(key_type, HotKeyType):
            self.__type = key_type
        else:
            raise TypeError('Wrong type, "key_type"s type must be "ShortCutType".')
        if not isinstance(keys, (list, tuple)):
            raise TypeError('Wrong type, "keys" must be a list or tuple, '
                            'and the type of its element must be "pynput.keyboard.Key", int or char.')
        if HotKeyType.SINGLE == self.__type and 1 < len(keys):
            raise ValueError('Invalid value, Single type hot key can only have one element.')
        if all([isinstance(key, Key) or key.isalpha() or key.isdigit() for key in keys]):
            self.__keys = [key if isinstance(key, Key) else KeyCode(char=key) for key in keys]
        if HotKeyType.SINGLE == self.__type:
            if isinstance(count, int) and 0 < count:
                self.__count = count
            else:
                raise ValueError('Invalid value, "count" must be a positive integer.')
            if isinstance(interval, float) and 0 < interval < 1:
                self.__interval = interval
            else:
                raise ValueError('Invalid value, "interval" must be between 0 and 1.')

    @property
    def trigger(self):
        return self.__trigger

    @property
    def type(self):
        return self.__type

    @property
    def keys(self):
        return self.__keys

    @property
    def count(self):
        return self.__count

    @property
    def interval(self):
        return self.__interval


class HotKeyManager:
    def __init__(self, trigger, keys, hot_key_type, count=2, interval=0.5):
        """
        :param trigger: Function called when hot key is triggered.
        :param list keys: Key list or tuple.
        :param HotKeyType hot_key_type: Shortcut type.
        :param int count: The press times of shortcut. Only for single key shortcut.
        :param float interval: The interval time between presses, unit: second. Only for single key shortcut.
        """
        if callable(trigger):
            self.__trigger = trigger
        else:
            raise TypeError('Wrong type, "trigger" must be a function.')
        self.__listener = Listener(on_press=self.__on_press, on_release=self.__on_release)
        self.type = hot_key_type
        self.keys = keys
        self.count = count
        self.interval = interval
        self.__pressed_keys = []
        self.__release_times = []

    def register_hotkey(self):
        pass

    def start(self):
        self.__listener.start()

    def stop(self):
        self.__listener.stop()

    def __on_press(self, key):
        if key in self.__keys:
            if HotKeyType.MULTIPLE == self.__type:
                self.__pressed_keys.append(key)
                if all([k in self.__pressed_keys for k in self.__keys]):
                    self.__trigger()

    def __on_release(self, key):
        if key in self.__keys:
            if HotKeyType.MULTIPLE == self.__type:
                self.__pressed_keys.remove(key)
            elif HotKeyType.SINGLE == self.__type:
                cur_time = time()
                if self.__release_times and self.__interval < cur_time - self.__release_times[-1]:
                    self.__release_times.clear()
                self.__release_times.append(cur_time)
                if self.__count == len(self.__release_times):
                    self.__release_times.clear()
                    self.__trigger()

    def check_status(self):
        if self.__listener.running:
            raise ValueError("Operation failed, the manager's already running.")

    @property
    def type(self):
        return self.__type

    @type.setter
    def type(self, value):
        self.check_status()
        if isinstance(value, HotKeyType):
            self.__type = value
        else:
            raise TypeError('Wrong type, "type"s type must be "ShortCutType".')

    @property
    def keys(self):
        return self.__keys

    @keys.setter
    def keys(self, value):
        self.check_status()
        if not isinstance(value, (list, tuple)):
            raise TypeError('Wrong type, "keys" must be a list or tuple, '
                            'and the type of its element must be "pynput.keyboard.Key", int or char.')
        if HotKeyType.SINGLE == self.__type and 1 < len(value):
            raise ValueError('Invalid value, Single type shortcut can only have one key.')
        if all([isinstance(key, Key) or key.isalpha() or key.isdigit() for key in value]):
            self.__keys = [key if isinstance(key, Key) else KeyCode(char=key) for key in value]

    @property
    def count(self):
        return self.__count

    @count.setter
    def count(self, value):
        self.check_status()
        if isinstance(value, int) and 0 < value:
            self.__count = value
        else:
            raise ValueError('Invalid value, "count" must be a positive integer.')

    @property
    def interval(self):
        return self.__interval

    @interval.setter
    def interval(self, value):
        self.check_status()
        if isinstance(value, float) and 0 < value < 1:
            self.__interval = value
        else:
            raise ValueError('Invalid value, "interval" must be between 0 and 1.')
