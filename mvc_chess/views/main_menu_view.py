from mvc_chess.views.base_view import BaseView


class MainMenuView:
    @classmethod
    def main_menu_view(cls):
        BaseView.base_view()
        print("1. List players")
        print("2. List tournaments")
        print("Q. Quit")
        return input("Choice : ")
