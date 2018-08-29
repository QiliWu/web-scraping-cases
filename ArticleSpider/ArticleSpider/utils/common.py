import hashlib

def get_md5(url):
    if isinstance(url, str):
        # 说明url是unicode字符，需要encoding,否则会报错：Unicode-objects must be encoded before hashing
        url = url.encode('utf-8')
    m = hashlib.md5()
    m.update(url)
    return m.hexdigest()

if __name__ == '__main__':
    print(get_md5('http://jobbole.com'))
    #结果：0efdf49af511fd88681529ef8c2e5fbf