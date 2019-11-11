import os
import sys


class Database(object):

    def __init__(self):
        # 获取当前路径
        current_dir = os.path.dirname(__file__)
        # 找到数据库目录
        DataDir = current_dir[:-2] + "Data"
        # 检查是否是文件夹
        isDir = os.path.isdir(DataDir)
        if isDir == False:
            print("current database data is not exists!")
            return False

        # 检查文档树是否存在
        DocumentDir = DataDir + "/Document"
        if os.path.isdir(DocumentDir) == False:
            print("DocumentDir is not exists")
            return False

        # 检查索引目录是否存在
        IndexDir = DataDir + "/Index"
        if os.path.isdir(IndexDir) == False:
            print("IndexDir is not exists")
            return False
        # 检查当前索引目录,记录当前最新的ID，也就是最后一个被创建的ID
        currentIndex = IndexDir + "/currentIndex.txt"
        if os.path.isfile(currentIndex) == False:
            print("currentIndex is not exists")
            return False
        # 建立索引树
        indexLog = IndexDir + "/IndexLog.txt"
        if os.path.isfile(indexLog) == False:
            print("indexLog is not exists")
            return False
        self.DocumentDir = DocumentDir
        self.IndexDir = IndexDir
        self.indexLog = indexLog
        self.currentIndex = currentIndex
        # 索引文件之间的间隔
        self.space = 50

    # 检查当前环境
    def searchIndexLog(self):
        # 找到索引树，查看的当前的位置，因为这个文件不会太大，所以可以直接读取所有行
        with open(self.indexLog, mode='r', encoding='utf-8') as fIndexLog:
            lines = fIndexLog.readlines()
        return lines

    # 进行调整内容
    def splitIndexLog(self,lines):
        if len(lines) == 0:
            last_line = ""
        else:
            # 读取最后一行内容
            last_line = lines[-1]
        if last_line == "" or last_line == "\n":
            last_line = []
        else:
            last_line = last_line.split(":")
        return last_line

    # 新增内容
    def add(self,title,content):
        # 找到当前最后的ID
        with open(self.currentIndex,mode='r',encoding='utf-8') as fCurrentIndex:
            lastIndex = fCurrentIndex.readline()
        # 给当前索引增加1
        newIndex = int(lastIndex) + 1
        # 直接写入文件
        with open(self.currentIndex,mode='w',encoding='utf-8') as fWriteCurrentIndex:
            fWriteCurrentIndex.write(str(newIndex))
        lines = self.searchIndexLog()
        file_index = self.splitIndexLog(lines)
        if len(file_index) == 0 and int(lastIndex) == 0:
            file_index = ['0','0','0000.log']
        elif len(file_index) == 0 and int(lastIndex) > 0:
            # 文件出错，回滚文件
            with open(self.currentIndex, mode='w', encoding='utf-8') as fWriteCurrentIndexs:
                fWriteCurrentIndexs.write(str(int(newIndex-1)))
            print("文件索引出错，请检查问题所在")
            return False
        file_title = int(file_index[2].split(".")[0])
        insertStr = ""
        file_log = ""
        if int(file_index[1]) < int(self.space):
            file_title = self.editFileIndex(file_title)
            file_log = str(file_title) + ".log"
            newLine = file_index[0] + ":" + str(newIndex) + ":" + file_log + "\n"
            if len(lines) == 0:
                insertStr = newLine
            else:
                lines[-1] = newLine
                for line in lines:
                    insertStr += line
        else:
            # 判断是否已经达到规定的50，规定一个文件只存贮50篇文章
            if int(file_index[1]) % int(self.space) == 0:
                # 文件索引加1
                file_title += 1
                file_title = self.editFileIndex(file_title)
                file_log = str(file_title) + ".log"
                # 如果是50的倍数，则另外起一行
                newLine = str(newIndex) + ":" + str(newIndex) + ":" + file_log + "\n"
                # 创建新的文件
                self.createNewFile(self.IndexDir + "/" + file_log)
                if len(lines) == 0:
                    insertStr = newLine
                else:
                    lines.append(newLine)
                    for line in lines:
                        insertStr += line
            else:
                file_title = self.editFileIndex(file_title)
                file_log = str(file_title) + ".log"
                newLine = file_index[0] + ":" + str(newIndex) + ":" + file_log + "\n"
                if len(lines) == 0:
                    insertStr = newLine
                else:
                    lines[-1] = newLine
                    for line in lines:
                        insertStr += line
        # 更新文件
        with open(self.indexLog,mode='w',encoding='utf-8') as fWriteIndexLog:
            fWriteIndexLog.write(insertStr)
        # 创建内容文件
        document_file = self.DocumentDir + "/"+ str(newIndex)+".txt"
        self.createNewFile(document_file)
        # 写入内容
        with open(document_file,"w",encoding="utf-8") as p:
            p.write(content)
        self.updateLogFile(self.IndexDir+"/"+file_log,newIndex,title)
        return newIndex
    # 更新log文件的内容
    def updateLogFile(self,fileName,Index,title):
        insertStr = str(Index)+":"+str(title)+":"+str(0)+"\n"
        with open(fileName,mode='a',encoding="utf-8") as f:
            f.write(insertStr)

    # 创建新的索引文件
    def createNewFile(self,fileName):
        if fileName == "":
            return False
        if not os.path.exists(fileName):
            with open(fileName,'w') as f:
                f.close()
            return True
        else:
            return False

    # 修改文件索引
    def editFileIndex(self,file_title):

        if len(str(file_title)) == 1:
            file_title = '000' + str(file_title)
        elif len(str(file_title)) == 2:
            file_title = '00' + str(file_title)
        elif len(str(file_title)) == 3:
            file_title = '0' + str(file_title)
        else:
            file_title = file_title
        return file_title

    # 读取indexLog文件
    def readIndexLog(self,Id):
        with open(self.indexLog,'r',encoding="utf-8") as f:
            data = f.readline()
            file_log = None
            while data:
                result = data.split(":")
                if int(result[0]) <= int(Id) <= int(result[1]):
                    res = result[2].split(".")
                    file_log = res[0]+ ".log"
                    break
                data = f.readline()
            return file_log

    # 查找logw文件
    def searchLog(self,file_log,Id):
        with open(self.IndexDir+"/"+file_log,mode='r',encoding="utf-8") as f:
            data = f.readline()
            result = []
            while data:
                res = data.split(":")
                if int(res[0]) == int(Id):
                    result = res
                data = f.readline()
            return result

    # 通过文件ID获取内容
    def get(self,Id):
        # 查询文件是否被删除
        # 查找文件所在位置
        IndexLogFile = self.readIndexLog(Id)
        result = self.searchLog(IndexLogFile,Id)
        ret = None
        if len(result) > 0:
            with open(self.DocumentDir+"/"+str(Id)+".txt") as f:
                ret = f.read()
        return ret

    # 修改文件内容
    def editContent(self,Id,content):
        log_dir = self.DocumentDir + "/" + str(Id) + ".txt"
        with open(log_dir,mode='w',encoding="utf-8") as f:
            f.write(content)
        return True

    # 修改文章标题
    def editTitle(self,Id,title):
        IndexLogFile = self.readIndexLog(Id)
        file_dir = self.IndexDir + "/" + IndexLogFile
        with open(file_dir, mode='r', encoding="utf-8") as f:
            lines = f.readlines()
        insertStr = ""
        for line in lines:
            rem = line.split(":")
            insertStr += line
            if int(rem[0]) == int(Id):
                insertStr = str(Id)+":"+str(title)+":"+str(rem[2])
        with open(file_dir,mode='w',encoding="utf-8") as w:
            w.write(insertStr)
        return True

    # 执行查询任务
    def query(self,sql):
        # 目前支持查询所有，支持limit查询,支持order by
        pass

    def select(self,orderBy='desc',Limit=50,page=1):
        with open(self.indexLog,mode='r',encoding="utf-8") as f:
            result = f.readline()
            # 获取开始位置
            index = result.split(":")[0]
            end = int(index)+int(Limit)
            # 声明一个装文件的集合
            collection_list = []
            while result:
                rem = result.split(":")
                if int(rem[0]) < end or int(rem[1]) < end:
                    collection_list.append(rem[2].split(".")[0])
                result = f.readline()
        # 读取文件
        title_list = {}
        for lin in collection_list:
            file_dir = self.IndexDir + "/" + lin + ".log"
            with open(file_dir,mode='r',encoding="utf-8") as f:
                res = f.readline()
                while res:
                    ret = res.split(":")
                    if int(ret[2]) == 0:
                        title_list[ret[0]]=ret[1]
                    res = f.readline()
        return title_list