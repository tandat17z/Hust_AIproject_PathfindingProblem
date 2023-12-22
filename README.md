# Hust_AIproject_PathfindingProblem
**- Yêu cầu:**
-  một số thư viện cần thiết: folium/chardet/bs4/django... (**pip install tên_thư_viện**)
- Quy trình:
  - Tiền xử lý dữ liệu (**cd preprocess_data**)
    - Chạy file main.py (**py main.py**)
    - Kết quả: trả ra file map.html -> Bản đồ hiển thị các con đường trong khu vực cần tìm kiếm
    - file map.html được chuyển tới website để chạy trên nền web
  - Thuật toán: ( in algorithm)
    - get_data (Xử lý dữ liệu):
      - get_road_data: Đọc file
      - get_nearest_road: tìm đường gần nhất với 1 điểm point
      - get_nearest_point: new_start (điểm gần nhất), point1, point2 (điểm thuộc đường)
      - get_children: Trả ra có nút kề
      - bfs
  - Chạy web ( **cd website**)
    - Chạy web (**py manage.py runserver**)
    - Đã hiển thị ra bản đồ vừa tạo được ở bước tiền xử lý
    - Hành động có thể thực hiện:
      1. Click vào vị trí bất kì trên bản đồ để chọn điểm bắt đầu, điểm kết thúc (Chú ý chỉ được click đc 2 lần nên nếu thao tác lại thì load lại trang )
      2. Trỏ tới các vị trí (Đường, icon,...) để xem thông tin
      3. Ấn Search để chuyển tới trang tìm kiếm (sẽ phải chờ 1 lúc để thuật toán chạy)
      4. Quan sát xong ấn quay lại để trở về trạng thái ban đầu
