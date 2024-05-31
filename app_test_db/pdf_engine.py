from fpdf import FPDF

def money_format(money):
    money_string = str(money)
    new_money_string = 'đ'
    # start format money string
    count = 0

    for char in reversed(money_string):
        if (count > 0) and (count % 3 == 0):
            new_money_string = '.' + new_money_string
        new_money_string = char + new_money_string
        count = count + 1

    return new_money_string

class PDF(FPDF):
    def add_centered_image(self, image_path):

        page_width = self.w
        image_width = 80
        x = (page_width - image_width) / 2

        self.set_x(x)
        self.image(image_path, x=x, y=None, w=image_width)


    def footer(self):
        pass

    def create_table(self, data, total):
        # Định nghĩa bảng
        self.set_font('NunitoBold', '', 12)

        cell_width_list = [15, 125 ,40]


        cell_width = 60
        cell_height = 10

        table_width = cell_width * len(data[0])
        table_height = cell_height * len(data)

        # Tính toán vị trí căn giữa dọc theo trục x
        page_width = self.w
        x = (page_width - table_width) / 2

        for row in data:
            self.ln()
            self.set_x(x)  # Thiết lập vị trí căn giữa dọc theo trục x cho mỗi hàng
            i = 0
            for item in row:
                self.cell(cell_width_list[i], cell_height, str(item), 1, 0, 'C')  # Vẽ nội dung bảng
                x += cell_width_list[i]  # Di chuyển đến vị trí tiếp theo trong cùng hàng
                i = i + 1
            x = (page_width - table_width) / 2  # Đặt lại vị trí căn giữa cho hàng mới


        self.ln()
        self.set_x(15)
        self.cell(40, 10, "Tổng tiền: ", 1, 0, 'C')

        self.cell(140, 10, f"{total}", 1, 0, 'C')
