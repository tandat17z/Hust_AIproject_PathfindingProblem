# Hust_AIproject_PathfindingProblem
- [Cài đặt](#cài-đặt)
- [Quy trình](#quy-trình)
- [Cách sử dụng](#cách-sử-dụng)
## :gear: Cài đặt
**1. Clone dự án từ GitHub:**
  ```bash
  git clone https://github.com/tandat17z/Hust_AIproject_PathfindingProblem.git
  ```
Tới thư mục làm việc của dự án. Ví dụ:
  ```bash
  cd D:\Hust_AIproject_PathfindingProblem
  ```
**2. Cài đặt các thư viện cần thiết:**
  ```bash
  pip install -r requirements.txt
  ```
Dự án cần sử dụng đến nhiều thư viện như: folium/shapely/geopandas/bs4/django...<br>
Tất cả chúng đầu được nếu cụ thể trong requirements.txt.<br>
**HOÀN THÀNH CÀI ĐẶT MÔI TRƯỜNG CHO DỰ ÁN** sau khi thực hiện xong lệnh trên.

## :airplane: Quy trình
### 1. Tiền xử lý dữ liệu:
  - Tới thư mục preprocess_data
  ```bash
  cd preprocess_data
  ```
  - Dữ liệu về khu vực cần tìm kiếm được lưu trong thư mục data. Đó là những file .geojson (là một định dạng tệp tin dữ liệu địa lý, sử dụng định dạng JSON để lưu thông tin địa lý). Bạn có thể download những file như vậy tại [overpass-turbo](https://overpass-turbo.eu/).
  -  Hàm **main.py** sẽ chứa những hàm để xử lý dữ liệu và thêm một vài tính năng để thu được file map.html để dùng cho website.
![image](https://github.com/tandat17z/Hust_AIproject_PathfindingProblem/assets_readme/main-py.png)
```bash
py main.py
```
### 2. Thuật toán:
  - Thuật toán tìm đường đi mà mình sử dụng là A star. Với thuật toán này sẽ luôn cho kết quả tối ưu trong dự án này. Những hàm liên quan phục vụ cho thuật toán được lưu trong folder **algorithm**:
    - module **func.py**:
      - get_oneway_id(file) -> list # Trả ra danh sách id những con đường 1 chiều
      - get_nearest_point(point, type) -> pointH, pointA, pointB
      - get_children(point)->list #Trả ra danh sách các node kề với point
  - module **A_star.py**:
      - search(start, target)-> list, list, list # Sử dụng thuật toán A* để tìm đường đi ngắn nhất từ start -> target
### 3. Tạo website:
  - Sử dụng framework Django để phát triển web nhanh chóng bằng python. Sử dụng file html đã tạo ở phần tiền xử lý để dùng làm giao diện cho web. Modules thuật toán sẽ được tính hợp để sử dụng tìm kiếm đường đi tại hai điểm bất kì khi sử dụng web.

## :anchor: Cách sử dụng:
  - Tới thư mục làm việc chứa website
  ```bash
  cd ../website
  ```
  - Khởi chạy máy chủ (được phát triển tích hợp trong Django) bằng lệnh dưới đây và ấn vào địa chỉ bên dưới để truy cập web. Giao diện web hiển thị bản đồ khu vực để chúng ta thực hiện các thao tác tiếp theo.
  ```bash
  py manage.py runserver
  ```
![image](https://github.com/tandat17z/Hust_AIproject_PathfindingProblem/assets/126872123/e74d02ed-a05c-4b02-8c1d-3edbf56f58f2)

  - Thao tác thực hiện:
      - Click lần lượt vào vị trí bất kì trên bản đồ để chọn điểm bắt đầu (start), điểm kết thúc (target) (Chú ý chỉ được click đc 2 lần theo đúng thứ tự nên nếu muốn thao tác lại thì  hãy load lại trang)
      - Có thể trỏ tới các con đường, icon để xem một vài thông tin của chúng.
      - Ấn **Search** để chuyển tới trang tìm kiếm (hãy chờ một chút để thuật toán tìm đường chạy)
      - Quan sát đường đi tìm đường tìm được (đường màu đỏ), xong ấn quay lại để trở về trang ban đầu.

