# -*- coding: utf-8 -*-
import logging,logging.handlers
import queue,string, json, datetime
import sys,os,random
from urllib.parse import unquote_plus,quote
from flask import Flask, request, jsonify, render_template, redirect, url_for, send_from_directory
import payment, checkWeb, dblib, notice_mail

app = Flask(__name__)

payment.test = True #---------------------------------------------------------------

@app.route('/')
def index():
    return render_template('index.html')
@app.route('/test')
def index_test():
    return render_template('index_test.html')

@app.route('/selling', methods=['POST'])
def selling():
    root_logger.info("/selling-----0-"+f"IP-method-url: {request.remote_addr} - {request.method} - {request.url}")
    data = request.form
    name = data.get(('name'), 'NULL').replace('_', '-')
    email = data.get(('email'), 'NULL@NULL.tw').replace('_', '-')
    #..............
    fee = 100 #calculate_fee(...)
    transaction_id = quote(name[0])+datetime.datetime.now().strftime("%y%m%d%H%M%S") + ''.join(random.choices(string.ascii_letters + string.digits, k=6))
    OrderedDict = {"transaction_id": transaction_id, "name": name, "email" : email, "fee": fee}
    try:
        return payment.ecpay(OrderedDict)
    except Exception as e:
        root_logger.error(e)
        return render_template('selling-Fail.html')

@app.route('/selling_test', methods=['GET', 'POST'])
def selling_test():
    #..............
    #..............
    #..............
    return render_template('selling-Success.html')

# ReturnURL: 綠界 Server 端回傳 (POST)
@app.route('/receive_result', methods=['POST'])
def ec_return():
    root_logger.info("/receive_result-----ecpay-"+f"IP-method-url: {request.remote_addr} - {request.method} - {request.url}")
    try:
        data1 = request.form
        check_mac_value = payment.get_mac_value(data1)
        if data1.get('CheckMacValue') != check_mac_value:
            print("RR--ERROR------ERROR-----------------ERROR----CheckMacValue---請聯繫管理員-------")
            return '1|OK'        
        # data1.get('RtnMsg') == 'paid')---------------------------------------------------------------
        result = True if (data1.get('RtnMsg') == '交易成功' or data1.get('RtnMsg') == 'paid') and data1.get('RtnCode') == '1' else False
        transaction_id = data1.get('MerchantTradeNo')
        TradeNo = data1.get('TradeNo')
        TradeDate = data1.get('TradeDate')
        fee = data1.get('TradeAmt')    
        name = data1.get('CustomField1')
        email = unquote_plus(data1.get('CustomField2'))
        org = data1.get('CustomField4')
        strdatas = data1.get('CustomField3').split("_")
        #..............
        #..............
        #..............
        date_format = "%Y/%m/%d %H:%M:%S"
        current_date = datetime.datetime.strptime(TradeDate, date_format) # datetime.datetime.now()
        # deadline = datetime.datetime(current_date.year, 8, 1)
        uniName = name+"_"+"_"+org+"_"+email+"_" #data1.get('Remark'] 
        data_receipt = {#...
        }
        # For test
        if payment.test or data1.get('SimulatePaid') == '1':
            print (result, data1.get('RtnMsg'), data1.get('RtnCode'),"-----------------")
            print("SimulatePaid receive_result-----------")#,re0,re
        # Real transaction
        else:    
            print (result, data1.get('RtnMsg'), data1.get('RtnCode'),"-----------------")
            db, cursor = dblib.connect_db()
            result_str=str(int(result))
            re0 = cursor.execute("INSERT INTO T_fee (transaction_id, name, email, ..., payment_status) VALUES (%s, %s, %s,..., %s)", (transaction_id, name, email, ..., fee, result_str))
            db.commit()
            cursor.close()
            db.close()
            print("Real receive_result-----------"+str(re0))
            #..............
            #..............
            #..............
            try:
                html_body = notice_mail.notice(data_receipt,...)
                checkWeb.send_email("Notice", html_body, email
                        ,attachment_path=[...])
            except Exception as e:
                root_logger.error(e)
    except Exception as e:
        root_logger.error(e)
    return '1|OK'


# OrderResultURL: 綠界 Client 端 (POST)
# @csrf.exempt
@app.route('/trad_result', methods=['GET', 'POST'])
def ec_user_page():
    print("/trad_result----------"+request.remote_addr+" - "+datetime.datetime.now().strftime("%y%m%d %H%M%S"))
    print(request.form.get('RtnMsg'))
    if request.method == 'GET':
        return redirect(url_for('index'))
    try:
        if request.method == 'POST':
            check_mac_value = payment.get_mac_value(request.form)
            data1 = request.form
            if data1.get('CheckMacValue') != check_mac_value:
                return render_template('Selling-Fail.html')
                #'請聯繫管理員-------'

            # 接收 ECpay 刷卡回傳資訊
            result = data1.get('RtnMsg') 
            transaction_id = data1.get('MerchantTradeNo')
            TradeNo = data1.get('TradeNo')
            TradeDate = data1.get('TradeDate')
            fee = data1.get('TradeAmt')    
            name = data1.get('CustomField1')
            email = unquote_plus(data1.get('CustomField2'))
            org = data1.get('CustomField4')
            strdatas = data1.get('CustomField3').split("_")
            #..............
            #..............
            #..............
            date_format = "%Y/%m/%d %H:%M:%S"
            current_date = datetime.datetime.strptime(TradeDate, date_format) # datetime.datetime.now()
            # deadline = datetime.datetime(current_date.year, 8, 1)
            uniName = name+"_"+"_"+org+"_"+email+"_" #data1.get('Remark'] 
            data_receipt = {#...
            }
            
            root_logger.info("trad_result-----0-"+f"IP-method-url: {request.remote_addr} - {request.method} - {request.url}")
            # 判斷成功
            print("/trad_result----------: ",data1.get('RtnMsg'), data1.get('RtnCode')) 
            if result == 'Succeeded' and data1.get('RtnCode') != '10300066':      
                return render_template('Selling-Success.html')

            elif result == 'Succeeded' and data1.get('RtnCode') == '10300066':            
                return render_template('success_confirming.html')#,
            # 判斷失敗
            else:
                print("/trad_result----------\n",data1.get('RtnMsg'), data1.get('RtnCode'))
                return render_template('Selling-Fail.html')
    except Exception as e:
        root_logger.error(e)
        return render_template('Selling-Fail.html')

@app.route('/check', methods=['GET'])
def check():
    return render_template('Selling-Check.html')
@app.route('/check_test', methods=['GET'])
def check_test():
    return render_template('Selling-Check_test.html')
@app.route('/check_status', methods=['POST'])
def check_status():
    print("check_status-----0-"+f"IP-method-url: {request.remote_addr} - {request.method} - {request.url}"+datetime.datetime.now().strftime("%y%m%d %H%M%S"))
    data = request.form
    #..............
    #..............
    #..............
    

def calculate_fee(Selling_type):
    # Logic to calculate fee based on current date and Selling details
    current_date = datetime.datetime.now()
    fee = 20000
    #..............
    #..............
    #..............    
    return fee

# def generate_transaction_id():
#     unique = False
#     db, cursor = dblib.connect_db()
#     while not unique:
#         transaction_id = ''.join(random.choices(string.ascii_letters + string.digits, k=20))
#         cursor.execute("SELECT transaction_id FROM fee WHERE transaction_id = %s", (transaction_id,))
#         if cursor.fetchone() is None:
#             unique = True
#     cursor.close()
#     db.close()
#     return transaction_id

log_queue = queue.Queue()
log_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# 設置文件處理器
file_handler = logging.FileHandler('./logs/app.log')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(log_format)
# 設置控制台處理器
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(log_format)
# 創建一個 QueueHandler 並將其添加到根記錄器
queue_handler = logging.handlers.QueueHandler(log_queue)
# 創建一個 QueueListener 並將其與文件處理器和控制台處理器關聯
queue_listener = logging.handlers.QueueListener(log_queue, file_handler, console_handler)
queue_listener.start()
root_logger = logging.getLogger()
root_logger.setLevel(logging.DEBUG)
if not any(isinstance(handler, logging.handlers.QueueHandler) for handler in root_logger.handlers):
    root_logger.addHandler(queue_handler)

@app.route('/favicon.ico')
@app.route('/robots.txt')
def favicon():
    return '', 204
@app.route('/image/<filename>')
def get_image(filename):
    try:
        return send_from_directory("./resources/images/", filename)
    except FileNotFoundError:
        return "Image not found", 404
    
@app.errorhandler(Exception)
def handle_exception(e):
    root_logger.error(f"Error occurred: {e}, IP-method-url: {request.remote_addr} - {request.method} - {request.url}")
    return str(e), 500

dblib.initialize_db()

# Below is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
if __name__ == '__main__':
    dblib.initialize_db()
    app.run(host="0.0.0.0",port=int("443"),threaded=True,ssl_context=('./SSL/yoursite/ssl.pem','./SSL/yoursite/privkey.pem')) #,ssl_context='adgn' ,debug=True
    # app.run(host="0.0.0.0",port=int("8080"),threaded=True) #,debug=True
