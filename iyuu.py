import requests
import json
from typing import Optional


class IYUUClient:
    """
    IYUU通知客户端
    用于发送通知到IYUU推送服务
    """
    
    def __init__(self, token: str):
        """
        初始化IYUU客户端
        
        Args:
            token: IYUU令牌
        """
        self.token = token
        self.base_url = f"https://iyuu.cn/{token}.send"
    
    def send_notification(self, text: str, desp: str) -> dict:
        """
        发送通知
        
        Args:
            text: 通知标题
            desp: 通知内容
            
        Returns:
            服务器响应的JSON字典
        """
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
        }
        
        data = {
            'text': text,
            'desp': desp
        }
        
        try:
            response = requests.post(
                self.base_url,
                headers=headers,
                data=data
            )
            
            # 返回响应的JSON
            try:
                return response.json()
            except json.JSONDecodeError:
                # 如果响应不是JSON格式，返回文本内容
                return {
                    'status_code': response.status_code,
                    'text': response.text
                }
                
        except requests.exceptions.RequestException as e:
            # 请求异常处理
            return {
                'error': str(e),
                'errcode': -1,
                'errmsg': 'Request failed'
            }
    
    def send_success_notification(self, title: str, content: str) -> dict:
        """
        发送成功通知的便捷方法
        
        Args:
            title: 通知标题
            content: 通知内容
            
        Returns:
            服务器响应的JSON字典
        """
        return self.send_notification(title, content)


def send_iyuu_notification(token: str, title: str, content: str) -> dict:
    """
    发送IYUU通知的便捷函数
    
    Args:
        token: IYUU令牌
        title: 通知标题
        content: 通知内容
        
    Returns:
        服务器响应的JSON字典
    """
    client = IYUUClient(token)
    return client.send_notification(title, content)


# 示例用法
if __name__ == "__main__":
    # 示例：使用实际的IYUU令牌
    token = "IYUU11697Td4d16339eb85a05868048a5b2b0643ba86d34907"
    
    # 发送通知
    result = send_iyuu_notification(
        token=token,
        title="测试通知",
        content="测试内容"
    )
    
    print("响应:", result)