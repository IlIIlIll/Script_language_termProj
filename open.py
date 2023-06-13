from PIL import Image, ImageTk
import tkinter as tk
import subprocess


class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("버스정보어플")

        # 부모 프레임 생성
        parent_frame = tk.Frame(self)
        parent_frame.pack()

        # 이미지 로드
        image = Image.open("Bus.jpg")

        # 이미지 크기 조정
        image = image.resize((400, 300))

        # 이미지를 표시하기 위해 ImageTk 객체로 변환
        self.img_tk = ImageTk.PhotoImage(image)

        # 이미지 라벨 위젯 생성하고 이미지 표시
        label = tk.Label(parent_frame, image=self.img_tk)
        label.pack(pady=10)

        # 시작 버튼 위치 지정
        start_button = tk.Button(parent_frame, text="시작", command=self.run_main)
        start_button.place(relx=0.5, rely=0.1, anchor=tk.CENTER)

        # 윈도우 크기 조정
        self.geometry("400x350")

    def run_main(self):
        # main.py 실행
        subprocess.run(["python", "main.py"])


if __name__ == "__main__":
    app = App()
    app.mainloop()
