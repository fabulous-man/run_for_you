import json
from PyQt6.QtWidgets import QListWidgetItem
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6.QtCore import Qt
def add_user_to_json(user_id, password, list_view):
    if user_id and password:  # 确保 user_id 和 password 都不为空
        new_user = {"user_id": user_id, "password": password}
        try:
            # 尝试读取已有的用户列表
            with open("user.json", "r") as file:
                users = json.load(file)
        except FileNotFoundError:
            # 如果 user.json 不存在，则创建一个新的列表
            users = []

        # 添加新用户到列表中
        users.append(new_user)

        # 将更新后的用户列表写回到 user.json 文件
        with open("user.json", "w") as file:
            json.dump(users, file, indent=4)

        # 刷新 listView
        refresh_list_view(list_view)

def refresh_list_view(list_view):
    model = QStandardItemModel(list_view)
    try:
        with open("user.json", "r") as file:
            users = json.load(file)
            for user in users:
                item = QStandardItem(user["user_id"])
                item.setCheckable(True)  # 使项目可以被选中
                item.setCheckState(Qt.CheckState.Unchecked)  # 默认未选中
                model.appendRow(item)
    except FileNotFoundError:
        pass

    list_view.setModel(model)

def delete_selected_users(list_view):
    model = list_view.model()
    checked_users = []
    for index in range(model.rowCount()):
        item = model.item(index)
        if item.checkState() == Qt.CheckState.Checked:
            checked_users.append(item.text())

    if not checked_users:
        return  # 如果没有用户被选中，则直接返回

    try:
        with open("user.json", "r") as file:
            users = json.load(file)
        # 保留未被选中的用户
        users = [user for user in users if user["user_id"] not in checked_users]
        with open("user.json", "w") as file:
            json.dump(users, file, indent=4)
    except FileNotFoundError:
        pass

    refresh_list_view(list_view)  # 刷新 listView 显示


def select_all_items(list_view):
    model = list_view.model()
    all_checked = True
    has_checked = False

    # 首先遍历所有项，判断是否全部选中或部分选中
    for i in range(model.rowCount()):
        item = model.item(i)
        if item.checkState() != Qt.CheckState.Checked:
            all_checked = False
        else:
            has_checked = True

    # 如果全部项都被选中，或者有部分项被选中但不是全部，则根据情况进行全选或全不选
    new_state = Qt.CheckState.Unchecked if all_checked else Qt.CheckState.Checked

    for i in range(model.rowCount()):
        item = model.item(i)
        item.setCheckState(new_state)



def load_selected_users(list_view):
    model = list_view.model()
    checked_users = []
    for index in range(model.rowCount()):
        item = model.item(index)
        if item.checkState() == Qt.CheckState.Checked:
            checked_users.append(item.text())

    if not checked_users:
        return  # 如果没有用户被选中，则直接返回

    try:
        with open("user.json", "r") as file:
            users = json.load(file)
        # 保留未被选中的用户
        users = [user for user in users if user["user_id"]  in checked_users]
        return users
    except FileNotFoundError:
        pass
