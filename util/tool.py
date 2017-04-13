from Crypto.Hash import MD5
def md5Obj(s):
    s = s.encode('UTF-8')
    md5obj=MD5.new()
    md5obj.update(s)
    return md5obj.hexdigest()
