module.exports = {
    port: 3000,         //启动端口
    DB_URL: 'mongodb://127.0.0.1:27017/meituan',    //数据库地址
    notifyUrl: 'http://192.168.31.156:3000/v1/notify_url',      //支付异步通知地址
    synNotifyUrl: 'http://39.108.3.12',              //客户端同步跳转
    sessionStorageURL: 'mongodb://127.0.0.1:27017/session',   //数据库存放session地址
    Bucket: 'zxxzxxzxx',   //七牛云bucket
    AccessKey: 'UyzsHG3QgS9QYPQGBrCaMUm3XKmq7SDz4HnND48d',   //七牛云accessKey
    SecretKey: '1KyLm0x0IUnmodFpd_WZthvV6gnoggF5-e4OYRaN',    //七牛云secretKey
    tencentkey: 'LA4BZ-MSZ6X-JUO4O-TJ76H-MNVIF-7TBGN',        //腾讯位置secreKey
    tencentkey2: 'XLJBZ-JWU34-ZX5US-XZAKI-5CCJ3-NUF2F',        //腾讯位置服务secreKey
    wechatAppid: '',  // 微信小程序appid
    wecahatSecret: '' // 微信小程序密钥
    
};


