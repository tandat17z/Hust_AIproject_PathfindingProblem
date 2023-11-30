# Hust_AIproject_PathfindingProblem
- Cài đặt một số thư viện cần thiết: folium/chardet/bs4/django... (**pip install tên_thư_viện**)
- Quy trình:
  - Tiền xử lý dữ liệu (**cd preprocess_data**)
    - Chạy file main.py (**py main.py**)
    - Kết quả: trả ra file map.html -> Bản đồ hiển thị các con đường trong khu vực cần tìm kiếm
    - file map.html được chuyển tới website để chạy trên nền web
  - Thuật toán: ( in algorithm)
    - (đang mô hình)
  - Chạy web ( **cd website**)
    - Chạy web (**py manage.py runserver**)
    - Đã hiển thị ra bản đồ vừa tạo được ở bước tiền xử lý
    - Hành động có thể thực hiện:
      1. Click vào vị trí trên bản đồ để chọn điểm bắt đầu, điểm kết thúc (Chú ý chỉ được click đc 2 lần nên nếu thao tác lại thì load lại trang )
      2. Trỏ tới các vị trí (Đường, icon,...) để xem thông tin
      3. Ấn Search để chuyển tới trang tìm kiếm (đang làm)
