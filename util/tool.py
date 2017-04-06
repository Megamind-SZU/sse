from Crypto.Hash import MD5
def md5Obj(s):
    md5obj=MD5.new()
    md5obj.update(s)
    return md5obj.hexdigest()
