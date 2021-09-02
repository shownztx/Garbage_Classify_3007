# 智慧垃圾桶项目

## 说明

本项目是一个带有前端界面的垃圾分类项目，加载了训练好的模型参数，模型为efficientnetb4，暂时为40分类问题。

 
## 运行环境

``` shell
pip install -r requirements.txt
```
注意：最新的opencv版本可能导致PyQt5无法正常运行，如遇到请降级。



## 快速开始

程序入口为main文件，pyqt5的界面为使用qt designer生成的。界面中核心的是4个控件，视频控件、计数控件、历史记录控件和分类结果对话框。
（在window.py中的class Ui_MainWindow中setupUi函数中的最后，做了计数控件、历史记录控件和模型、标签的加载）

### 视频控件
使用cv2抓取摄像头视频，并显示在videoLayout中的label控件label上。（名字就叫label..）（在main函数中使用语句 camera = Camera(1)  # 0为笔记本自带摄像头 1为USB摄像头 抓取视频画面。）
以下是Ui_MainWindow类中与视频显示相关的部分：（如果部署在树莓派上，此处需要改动）
``` python
class Ui_MainWindow(object):

    def __init__(self, camera):
        self.camera = camera
        # Create a timer.
        self.timer = QTimer()
        self.timer.timeout.connect(self.nextFrameSlot)
        self.start()

    def start(self):
        self.camera.openCamera()
        self.timer.start(1000. / 24)

    def nextFrameSlot(self):
        rval, frame = self.camera.vc.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = QImage(frame, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(image)
        self.label.setPixmap(pixmap)
```
### 计数控件
读取保存在static/CSV/count.csv文件中的分类次数，并显示在countLayout中的label控件count上。初始状态的static/CSV/count.csv文件为只有一个0。

### 历史记录控件
读取保存在static/CSV/history.csv文件中的历史记录（第一列为分类结果，第二列为照片路径），并显示在listLayout中的QListWidget控件listWidget上。初始状态的static/CSV/history.csv文件为空。
这里只显示了最近15条记录，代码在csv_utils.py中的read_history_csv函数。
### 分类结果对话框
触发次对话框的条件是点击界面上的pushButton（绑定代码位于window.py中的class Ui_MainWindow中setupUi函数），触发的函数为class Ui_MainWindow中的show_dialog函数。如果部署在树莓派上可改为由距离传感器触发。
``` python
  self.pushButton.clicked.connect(self.show_dialog)
```
 这部分的核心就是show_dialog函数。要实现拍照，调用分类模型，在对话框关闭后还实现了主界面计数控件和历史记录控件的更新。（耦合性较大..）
文件的保存方面只是使用了CSV文件来保存计数、结果和照片路径。（初始状态的static/CSV/count.csv文件为只有一个0。初始状态的static/CSV/history.csv文件为空。）
``` python
    def show_dialog(self):
        count_csv_path = "static/CSV/count.csv"  # 计数
        history_csv_path = "static/CSV/history.csv"  # 历史记录
        image_path = "static/photos/"  # 照片目录
        classification = "test"  # 测试用的

        timeout = 4 # 对话框停留时间
        ret, frame = self.camera.vc.read()  # 拍照
        self.history_photo_num = self.history_photo_num + 1  # 照片自增命名
        image_path = image_path + str(self.history_photo_num) + ".jpg"  # 保存照片的路径
        cv2.imwrite(image_path, frame)  # 保存
        # time.sleep(1)

        image = utils.load_image(image_path)
        classify_model = self.classify_model  # 模型、标签的初始化在setupUi函数最后
        label_to_content = self.label_to_content
        prediction, label = classify_image(image, classify_model) # 调用模型

        print('-' * 100)
        print(f'Test one image: {image_path}')
        print(f'classification: {label_to_content[str(label)]}\nconfidence: {prediction[0, label]}')
        print('-' * 100)

        classification = str(label_to_content[str(label)])  # 分类结果
        confidence = str(f'{prediction[0, label]}')  # 置信度
        confidence = confidence[0:5]  # 保留三位小数
        self.dialog = Dialog(timeout=timeout, classification=classification, confidence=confidence)  # 传入结果和置信度
        self.dialog.show()
        self.dialog.exec() # 对话框退出

        # 更新历史记录中count数目
        count_list = read_count_csv(filename=count_csv_path)
        count = int(count_list[0]) + 1
        self.count.setText(str(count))
        write_count_csv(filename=count_csv_path, count=count)

        # 更新历史记录
        write_history_csv(history_csv_path, classification=classification, photo_path=image_path)
        self.listWidget.clear()
        history_list = read_history_csv(history_csv_path)
        for record in history_list:  # 每次都是全部重新加载，效率较低...
            item = QtWidgets.QListWidgetItem(QtGui.QIcon(record[1]), record[0])  # 0为类别，1为图片路径
            self.listWidget.addItem(item)
```

## TODO List

- 完成树莓派端部署
- 完成模型云端部署
