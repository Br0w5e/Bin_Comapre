#python3
#by Br0w5e
import hashlib
import base64
import os
import sys
#计算md5值，返回md5值
def md5block(filename, start, end):
    #定义读取区块大小
    sizeblock = 1024 * 1024 * 100

    with open(filename, 'rb') as f:
        md5 = hashlib.md5()
        f.seek(start)
        while f.tell() < (end - sizeblock):
            data = f.read(sizeblock)
            md5.update(data)
        data = f.read(end - f.tell())
        md5.update(data)
        retmd5 = md5.hexdigest()

        return retmd5

#二分法比较，返回diff起始位置，大区间
def diffFile(Filename_1, Filename_2):
    #读取文件大小
    size_1 = os.path.getsize(Filename_1)
    size_2 = os.path.getsize(Filename_2)

    #取得的最大值，考虑最简单的问题，其他不考虑
    max_size = max(size_1, size_2)

    #给出比较数组，记录位置，并将数组长度填充进去。
    diff = []
    diff.append((0, max_size))

    #二分法开始比较
    while diff != []:
        #将长度pop出来，后边要用的。
        i = diff.pop(0)

        #确定起始位置
        s_pos = int(i[0])
        e_pos = s_pos + int(((i[1] - i[0]) / 2) + 1)

        #计算两段hash,前半部分
        h_f1 =  md5block(Filename_1, s_pos, e_pos)
        h_f2 =  md5block(Filename_2, s_pos, e_pos)

        #二分的两部分hash不相等,不断标记不同的位置。
        if h_f1 != h_f2:
            diff.append((s_pos, e_pos))

        #相等的情况下,继续运行 后半部分
        h_f1 = md5block(Filename_1, e_pos, i[1])
        h_f2 = md5block(Filename_2, e_pos, i[1])

        if h_f1 != h_f2:
            diff.append((e_pos, i[1]))
        #小于1024就停止二分法
        if diff[0][1] - diff[0][0] <= 1024:
            break
    return diff

# 不同的区间，返回不同区间组成的列表
def diffInterval(diff, Filename_1, Filename_2):
    #开始逐比特比较
    #比较结果存储在数组中
    ret  = []  #不同的区间
    #res = []   #不同的对应值

    with open(Filename_1, 'rb') as f1, open(Filename_2, 'rb') as f2:
        for i in diff:
            #寻找起始位置
            f1.seek(i[0])
            f2.seek(i[0])

            #读取指定长度
            s1 = f1.read(i[1] - i[0])
            s2 = f2.read(i[1] - i[0])

            s_pos = 0
            #j = 0
            # 比较返回不同的起始位置和值
            while s_pos < len(s1):
                if s1[s_pos] != s2[s_pos]:
                    e_pos = s_pos
                    while s1[e_pos] != s2[e_pos]:
                        e_pos += 1
                    #将不同的作为元组添加进 ret中
                    ret.append((i[0] + s_pos, i[0] + e_pos))
                    s_pos = e_pos
                s_pos += 1          
    return ret

# 不同的内容，返回不同内容组成的列表，以元组表示。
def diffContent(ret, Filename_1, Filename_2):
    #不同的结果
    res = []
    with open(Filename_1, 'rb') as f1, open(Filename_2, 'rb') as f2:
        for i in ret:
            #寻找起始位置
            f1.seek(i[0])
            f2.seek(i[0])

            #读取指定长度，并将其添加到列表
            s1 = f1.read(i[1] - i[0])
            s2 = f2.read(i[1] - i[0])
            res.append((s1, s2))
    return res

#生成test文件
def test():
    with open('1', 'w') as f1, open('2', 'w') as f2:
        for i in range(10000000):
            if i == 64363:
                f1.write('aaas')
                f2.write('bbbd')
            else:
                f1.write(str(1))
                f2.write(str(1))

"""
#测试
diff = diffFile('1', '2')
ret = diffInterval(diff, '1', '2')
res = diffContent(ret, '1', '2')
print(ret, res)
"""
# main函数
def main():
    #test()
    if len(sys.argv) != 3:
        print("Arg Error!!!!!!")
        print("Usage: python3 bin_compare.py filename1 filename2")
        sys.exit()
    Filename_1 = sys.argv[1]
    Filename_2 = sys.argv[2]
    #求diff
    diff = diffFile(Filename_1, Filename_2)
    #求区间
    ret = diffInterval(diff, Filename_1, Filename_2)
    #求内容
    res = diffContent(ret, Filename_1, Filename_2)
    print(diff)
    print(ret, res)
    #print(res)

if __name__ == "__main__":
    main()
