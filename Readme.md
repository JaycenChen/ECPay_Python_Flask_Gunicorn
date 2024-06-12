# Ecpay Flask (綠界支付) 介接
**For 簡易部署 (gunicorn production部署)： 2024-06-13**

簡單可用的綠界金流(以信用卡為例)串接項目，結構相對完整，可根據需要進行二次開發

### 本項目的金流串接主要包含

* 創建訂單 (根據前端回傳資料，介接到綠界支付返回給用戶支付)
* 接受處理綠界支付結果 (對Server端) 回傳 (POST/**ReturnURL**)
    * 給綠界返回'1|OK'
    * 注意若未正確回應1|OK，綠界會隔5~15分鐘後重發訊息，當天重複發送四次。
        * [RtnMsg] 會 變成 'paid'
* 接受處理綠界支付結果 (透過Client端) 回傳 (POST/**OrderResultURL**)
    * 注意檢查macvalue
    * 給用戶返回結果頁面/...


## 使用說明：
- 測試環境：[測試資訊](https://developers.ecpay.com.tw/?p=2856)
- 介接注意事項(只支援**https協議443端口**)：[注意事項](https://developers.ecpay.com.tw/?p=2858)
### 環境
* Python (3.8.10) 
* flask (3.0.3)
* Flask-MySQLdb (2.0.0)
### 使用gunicorn啟動串接網站部署
```
gunicorn -c gunicorn.py AllOne:app
```

### 使用checkWeb啟動網站監視
```
python3 checkWeb.py
```

## 目錄結構說明

**gunicorn.py - 程式啟動入口**

```
filetree 
├── /files/
├── /logs/
├── /resources/
├── /sdk/
├── /SSL/
├── /static/
├── /templates/
├── AllOne.py - 主要功能與Flask路由檔案
├── checkWeb.py - 可獨立運行，網站活動性檢測 & html郵件寄送function
├── dblib.py - 資料庫相關function
├── gunicorn.py - 程式啟動入口
├── LICENSE.txt
├── payment.py - 與綠界交互和驗證的function
├── README.md
└── redirect.py - 獨立運行，重定向：80/.. => 443
```
### ![綠界付款流程圖](https://developers.ecpay.com.tw/wp-content/uploads/2022/01/%E5%85%A8%E6%96%B9%E4%BD%8D%E4%BB%98%E6%AC%BE%E4%BA%A4%E6%98%93%E6%B5%81%E7%A8%8B2022-5-1024x727.png)

