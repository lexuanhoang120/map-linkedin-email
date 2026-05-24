Hướng dẫn kiểm tra và lấy thông tin việc email có tài khoản linkedin hay không?

## Chuẩn bị
- Cài đặt Python
- Setup môi trường ảo
- Cài đặt các thư viện cần thiết
- Cài đặt chromedriver
- Cài đặt tài khoản outlook tại đường dẫn ./resource/account.txt
- Cài đặt email cần kiểm tra tại đường dẫn ./resource/email.xlsx
- Cài đặt chromedriver tại đường dẫn ./resource/chromedriver (phiên bản hiện tại là 114.x.x)


## Tiến hành chạy
### Bước 1
- Cập nhập thông tin tài khoản outlook tại ./resource/account.txt
- Cập nhập thông tin email cần kiểm tra tại ./resource/email.xlsx
- Kiểm tra và cập nhập phiên bản chromedriver tại ./resource/chromedriver

### Bước 2
- Mở terminal và chạy lệnh sau:
```bash
python 1_get_token_from_outlook.py
```
- Mục đích: lấy tất cả token từ tài khoản outlook đã cài đặt tại ./resource/account.txt và lưu tại file access_token.json

### Bước 3
- Mở terminal và chạy lệnh sau:
```bash
python 2_email_in_linkedin.py
```
- Mục đích: kiểm tra email có tài khoản linkedin hay không và lưu kết quả tại file email_match_linkedin.json, tùy thuộc vào đặc tính của tài khoản outlook mà kết quả có thể khác nhau (chi tiết xem thêm file .pdf)

### Kết quả
- Kết quả sẽ được lưu tại file email_match_linkedin.json


 **Lưu ý**: Xem thêm file .pdf và main.ipynb để biết thêm chi tiết. 
