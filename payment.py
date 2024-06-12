# -*- coding: utf-8 -*-
from flask import Flask, render_template, jsonify, request, session, redirect, Blueprint, url_for
from werkzeug.security import generate_password_hash, check_password_hash
import importlib.util
import os,time
from datetime import datetime
import pprint
import collections, json, hashlib
from urllib.parse import quote_plus


# 導入 ECpay SDK
import importlib.util
filename = os.path.dirname(os.path.realpath(__file__))
spec = importlib.util.spec_from_file_location(
    "ecpay_payment_sdk", filename + "/sdk/ecpay_payment_sdk.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


test =True 
host_name = 'https://yoursite/'
payment = Blueprint('payment', __name__)
HashKey='yourreal_key'
HashIV='yourreal_iv'
if test:
    HashKey='pwFHCqoQZGmho4w6'
    HashIV='EkRm7iFT261dpevs'


def order_search(transaction_id):
    global test,HashKey,HashIV
    order_search_params = {
        'MerchantTradeNo': transaction_id, #OrderedDict.get('transaction_id'),
        'TimeStamp': int(time.time())
    }

    # 建立實體
    ecpay_payment_sdk = module.ECPayPaymentSdk(
        MerchantID='ID...',
        HashKey=HashKey,
        HashIV=HashIV
        )

    try:
        # 介接路徑
        query_url =""
        if test: query_url = 'https://payment-stage.ecpay.com.tw/Cashier/QueryTradeInfo/V5'  # 測試環境
        else: query_url = 'https://payment.ecpay.com.tw/Cashier/QueryTradeInfo/V5' # 正式環境

        # 查詢訂單
        query_result = ecpay_payment_sdk.order_search(
            action_url=query_url,
            client_parameters=order_search_params)
        pprint.pprint(query_result)
        return query_result
    except Exception as error:
        print('An exception happened: ' + str(error))

# 建立訂單後跳轉至 ECpay 頁面
def ecpay(OrderedDict):
    global test,host_name,HashKey,HashIV
    safe_characters = '-_.!*()'
    CustomField1 = OrderedDict.get('name')
    # CustomField2 =  quote_plus(OrderedDict.get('email'), safe=safe_characters)
    # CustomField3 = OrderedDict.get('...')+"_"+ OrderedDict.get('paper_id')+"_"+ "..."
    # CustomField4 = OrderedDict.get('...')
    # 設定傳送給綠界參數
    order_params = {
        'MerchantTradeNo': OrderedDict.get('transaction_id'),
        'StoreID': '',
        'MerchantTradeDate': datetime.now().strftime("%Y/%m/%d %H:%M:%S"),
        'PaymentType': 'aio',
        'TotalAmount': OrderedDict.get('fee'),
        'TradeDesc': 'WOCC2024',
        'ItemName': OrderedDict.get('name') + ' fee',
        'ReturnURL': host_name + '/receive_result',
        'ChoosePayment': 'Credit',
        'ClientBackURL': host_name + '/trad_result',
        'ItemURL': host_name,
        'Remark': OrderedDict.get('name')+"_"+OrderedDict.get('...')+"_"+OrderedDict.get('paper_id')+"_"+OrderedDict.get('email'),
        'ChooseSubPayment': '',
        'OrderResultURL': host_name + '/trad_result',
        'NeedExtraPaidInfo': 'Y',
        'DeviceSource': '',
        'IgnorePayment': '',
        'PlatformID': '',
        'InvoiceMark': 'N',
        'CustomField1': CustomField1, #str(tid),
        'CustomField2': '',#CustomField2,
        'CustomField3': '',#CustomField3,
        'CustomField4': '',#CustomField4,
        'EncryptType': 1,
    }

    inv_params = {
        # 'RelateNumber': 'Tea0001', # 特店自訂編號
        # 'CustomerID': 'TEA_0000001', # 客戶編號
        # 'CustomerIdentifier': '53348111', # 統一編號
        # 'CustomerName': '客戶名稱',
        # 'CustomerAddr': '客戶地址',
        # 'CustomerPhone': '0912345678', # 客戶手機號碼
        # 'CustomerEmail': 'abc@ecpay.com.tw',
        # 'ClearanceMark': '2', # 通關方式
        # 'TaxType': '1', # 課稅類別
        # 'CarruerType': '', # 載具類別
        # 'CarruerNum': '', # 載具編號
        # 'Donation': '1', # 捐贈註記
        # 'LoveCode': '168001', # 捐贈碼
        # 'Print': '1',
        # 'InvoiceItemName': '測試商品1|測試商品2',
        # 'InvoiceItemCount': '2|3',
        # 'InvoiceItemWord': '個|包',
        # 'InvoiceItemPrice': '35|10',
        # 'InvoiceItemTaxType': '1|1',
        # 'InvoiceRemark': '測試商品1的說明|測試商品2的說明',
        # 'DelayDay': '0', # 延遲天數
        # 'InvType': '07', # 字軌類別
    }

    extend_params_1 = {
        'ExpireDate': 7,
        'PaymentInfoURL': 'https://www.ecpay.com.tw/payment_info_url.php',
        'ClientRedirectURL': '',
    }

    extend_params_2 = {
        'StoreExpireDate': 15,
        'Desc_1': '',
        'Desc_2': '',
        'Desc_3': '',
        'Desc_4': '',
        'PaymentInfoURL': 'https://www.ecpay.com.tw/payment_info_url.php',
        'ClientRedirectURL': '',
    }

    extend_params_3 = {
        'BindingCard': 0,
        'MerchantMemberID': '',
    }

    extend_params_4 = {
        'Redeem': 'N',
        'UnionPay': 0,
    }
    # 建立ecpay實體
    ecpay_payment_sdk = module.ECPayPaymentSdk(
        MerchantID='ID...',
        HashKey=HashKey,
        HashIV=HashIV
        )

    # 合併延伸參數
    # order_params.update(extend_params_1)
    # order_params.update(extend_params_2)
    order_params.update(extend_params_3)
    order_params.update(extend_params_4)
    # 合併發票參數
    order_params.update(inv_params)

    try:
        # 產生綠界訂單所需參數
        final_order_params = ecpay_payment_sdk.create_order(order_params)
        action_url = ""
        # 產生不同環境下 html 的 form 格式
        if test:action_url = 'https://payment-stage.ecpay.com.tw/Cashier/AioCheckOut/V5'  # 測試環境
        else: action_url = 'https://payment.ecpay.com.tw/Cashier/AioCheckOut/V5' # 正式環境
        html = ecpay_payment_sdk.gen_html_post_form(action_url,
                                                    final_order_params)
        print("1-2-------------------------0")
        return html

    except Exception as error:
        print('An exception happened: ' + error)


# 驗證付款結果附帶的 check_mac_value，支付安全
def get_mac_value(request_form):
    global test,HashKey,HashIV
    params = dict(request_form)
    if params.get('CheckMacValue'):
        params.pop('CheckMacValue')
    ordered_params = collections.OrderedDict(sorted(params.items(), key=lambda k: k[0].lower()))
    encoding_list = []
    encoding_list.append('HashKey=%s&' % HashKey)
    encoding_list.append(''.join(['{}={}&'.format(key, value) for key, value in ordered_params.items()]))
    encoding_list.append('HashIV=%s' % HashIV)
    safe_characters = '-_.!*()'
    encoding_str = ''.join(encoding_list)
    encoding_str = quote_plus(str(encoding_str), safe=safe_characters).lower()
    check_mac_value = hashlib.sha256(encoding_str.encode('utf-8')).hexdigest().upper()

    return check_mac_value