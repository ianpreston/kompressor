from kompressor.io import IoState, IoMethod


class SetSlot(IoMethod):
    def activate(self):
        message = IoState.current_frame()
        slot_name = message.args[0]
        slot_value = message.args[1]

        message.target.set_slot(slot_name, slot_value)
        return slot_value


class Clone(IoMethod):
    def activate(self):
        target = IoState.current_frame().target
        return target.clone()


class Println(IoMethod):
    def activate(self):
        target = IoState.current_frame().target
        print(target.get_slot('value'))
        return target.get_slot('value')
