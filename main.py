#Import modules
from PyQt5.QtCore import Qt,QObject,pyqtSignal,QThread
from PyQt5.QtWidgets import QApplication,QWidget,QFormLayout,QVBoxLayout,QHBoxLayout,QLabel,QPushButton,QLineEdit,QComboBox,QRadioButton,QButtonGroup,QProgressBar
from PyQt5.QtWidgets import QFileDialog,QMessageBox
from PyQt5.QtGui import QPixmap
from yt_dlp.utils import DownloadError, ExtractorError
import sys, os
import yt_dlp


def resource_path(relative_path):
    """ Get absolute path to resource (works for dev and for PyInstaller exe) """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

class App(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("ytDownloader By KevalG69")
        self.resize(500,250)

        self.master_layout = QVBoxLayout()
        self._max_percent = 0
        #loader

            #creating overlay to cover whole window
        self.overlay = QWidget(self)
        self.overlay2 = QWidget(self)
            #setting style
        self.overlay.setStyleSheet("background-color: rgba(0, 0, 0, 190); font-weight:bold;")
        self.overlay2.setStyleSheet("background-color: rgba(0, 0, 0, 190); font-weight:bold;")

            #cover whole window
      
            #block other input
        self.overlay.setAttribute(Qt.WA_TransparentForMouseEvents,False)
        self.overlay2.setAttribute(Qt.WA_TransparentForMouseEvents,False)

            #inside overlay
        self.layout = QVBoxLayout(self.overlay)
        self.layout2 = QVBoxLayout(self.overlay2)

        self.layout.setAlignment(Qt.AlignCenter)
        self.layout2.setAlignment(Qt.AlignCenter)

        self.loader_label = QLabel()
        self.loader_text = QLabel("Wait while we are stealing from the cloud...")
        self.loader_label.setAlignment(Qt.AlignCenter)
        self.loader_text.setAlignment(Qt.AlignCenter)
    
            #setting gif in the loader label
        self.pixmap = QPixmap(resource_path("waiting.jpg"))
        self.sizeAdjustedPixmap = self.pixmap.scaled(180,120,Qt.KeepAspectRatio,Qt.SmoothTransformation)
        self.loader_label.setPixmap(self.sizeAdjustedPixmap)
        
            #setting loader to ther overlay
        self.layout.addWidget(self.loader_label)
        self.layout.addWidget(self.loader_text)
        
        
            #hide overlay
        self.overlay.hide()


        #creating form 
        self.form_layout = QFormLayout()
        self.form_layout.setLabelAlignment(Qt.AlignRight)

     
        #creating labels
        self.url_label = QLabel("Video URL :")
        self.type_label = QLabel("Type :")
        self.format_label = QLabel("Format :")
        self.quality_label = QLabel("Quality :")
        self.location_label = QLabel("Location :")
        self.progress_label = QLabel("")

        #creating buttons
        self.browse_button = QPushButton("Browse")
            #giving name for style
        self.browse_button.setObjectName("browseButton")
        self.download_button = QPushButton("Download")
        self.download_button.setObjectName("downloadButton")
    
        #creating text input
        self.url_input = QLineEdit()
        self.location_input = QLineEdit()
        
        #creating combobox
        self.format_combobox = QComboBox()
        self.quality_combobox = QComboBox()
        
            #audio formats
        audioFormats = ["Original (Best)","MP3","AAC","WAV","FLAC","OGG"]

            #adding formats
        self.format_combobox.addItems(audioFormats)


        #Radio Buttons
        self.video_radio = QRadioButton("Video")
        self.audio_radio = QRadioButton("Audio")

        #check video by default
        self.video_radio.setChecked(True)
            #group buttons
        self.radio_group = QButtonGroup(self)
        self.radio_group.addButton(self.video_radio)
        self.radio_group.addButton(self.audio_radio)

        #Progress bar
        self.download_progress = QProgressBar()
        
            #set value
        self.download_progress.setValue(0)


        #arranging items

            #url 
        # self.url_row = QHBoxLayout()
        # self.url_row.addWidget(self.url_label)
        # self.url_row.addWidget(self.url_input)
        self.form_layout.addRow(self.url_label,self.url_input)
        
            #type
        self.type_widget = QWidget()
        self.type_layout = QHBoxLayout(self.type_widget)
        self.type_layout.setSpacing(1)
        self.type_layout.addWidget(self.video_radio)
        self.type_layout.addWidget(self.audio_radio)

        self.form_layout.addRow(self.type_label,self.type_widget)

            #Quality
        # self.quality_row = QHBoxLayout()
        # self.quality_row.addWidget(self.quality_label)
        self.form_layout.addRow(self.quality_label,self.quality_combobox)

            #format
        # self.format_row = QHBoxLayout()
        # self.format_row.addWidget(self.format_label)
        # self.format_row.addWidget(self.format_combobox)
        self.form_layout.addRow(self.format_label,self.format_combobox)
        
            #location
        self.location_row = QHBoxLayout()
       
        self.location_row.addWidget(self.location_input)
        self.location_row.addWidget(self.browse_button)
        self.location_row.setSpacing(8)
        self.form_layout.addRow(self.location_label,self.location_row)

            #download
        self.download_row = QHBoxLayout()
        self.download_row.addStretch(1)
        self.download_row.addWidget(self.download_button)
        self.download_row.addStretch(1)
        self.download_button.setFixedSize(136,48)
        self.form_layout.addRow(self.download_row)

            #progressbar
        
        self.layout2.addStretch(1)
        self.layout2.addWidget(self.download_progress)
        self.layout2.addWidget(self.progress_label)
        self.progress_label.setAlignment(Qt.AlignRight)
        self.download_progress.setMinimumWidth(468)
        self.layout2.addStretch(1)

        self.download_progress.setVisible(False)
        self.progress_label.setVisible(False)


        self.overlay2.hide()
        #adding progress bar to the layout       

        #adding all layout to master layout
        # self.master_layout.addLayout(self.url_row)
        # self.master_layout.addLayout(self.type_row)
        # self.master_layout.addLayout(self.format_row)
        # self.master_layout.addLayout(self.quality_row)
        # self.master_layout.addLayout(self.location_row)
        # self.master_layout.addLayout(self.download_row)
        # self.master_layout.addLayout(self.progress_row)

        self.form_layout.setVerticalSpacing(24)

        #adding event to the widgets
            #radio toggle
        self.video_radio.toggled.connect(self.on_radio_change)
        self.audio_radio.toggled.connect(self.on_radio_change)

            #when text in input changes
        self.url_input.textChanged.connect(self.on_radio_change)

            #when browse button clicked
        self.browse_button.clicked.connect(self.browse_folder)

            #when donwload clicked
        self.download_button.clicked.connect(self.download)

        self.format_label.setVisible(False)
        self.format_combobox.setVisible(False)


        self.overlay.setGeometry(self.rect())
        self.overlay2.setGeometry(self.rect())
        #set to main layout
        self.setLayout(self.form_layout) 


        #adding style
        self.setStyleSheet(""" 
            QWidget{
                background-color:#121212;
                color:#ffffff;
                font-family:Arial;
                font-size:16px;         
            }
            
            QLabel{
                font-size:16px;
            }
            QLineEdit{
                background-color:#282828;
                width:280px;
                height:32px;
                border-radius:8px;
            }
            QLineEdit:focus {
                border: 1px solid #1ed760;
                background-color: #333333;
            }
            QRadioButton{
                spacing:8px;
            }
            QRadioButton::indicator{
                width:14px;
                height:14px;
                border-radius:7px;
                border:2px solid #1db954;               
            }
            QRadioButton::indicator:checked {
                background: #1db954;
            }
            QComboBox{
                background-color:#282828;   
                height:32px;    
                border-radius:8px;              
            }
            QPushButton {
                background-color: #1db954;
                color: white;
                border-radius: 8px;
               
            }
            QPushButton#browseButton{
                width:96px;
                height:32px;
                           font-weight:bold;  
                font-size:16px
            }
            QPushButton#downloadButton{
                font-weight:bold;           
                font-size:16px
            }
            QPushButton:hover {
                background-color: #1ed760;
            }
            QPushButton:pressed {
                background-color: #1aa34a;
            }
            
            QProgressBar {
                border: 1px solid #444;
                border-radius: 6px;
                background: #1e1e1e;
                text-align: center;
                height: 20px;
            }

            QProgressBar::chunk {
                background-color: #1db954;
                border-radius: 6px;
            }
           
        """)


        #adding event to the widgets
        
   

    #function to get the format and quality available in video
    def get_format_of_video(self,url):

        try:

            #tell yt_dl to send all formats
            #create dictionary of options
            ydl_options = {"listformats":True}

            with yt_dlp.YoutubeDL(ydl_options) as ydl:
                
                #extract info from api
                info = ydl.extract_info(url,download=False)

                #get formats if exist otherwise store empty array
                formats = info.get("formats",[])

                #storing formats
                video_formats =[]
                audio_formats =[]

                #loop through all formats
                for format in formats:
                
                    vcodec = format.get("vcodec")
                    acodec = format.get("acodec")

                    #if format is video
                    if vcodec != "none":
                        #get resolution
                        resolution = format.get("format_note") or format.get("height")
                        #get fps
                        fps = format.get("fps")
                        video_formats.append({
                        "format_id": format["format_id"],
                        "resolution": f"{resolution}p {fps}fps" if fps else f"{resolution}p",
                        "ext": format["ext"],
                        "filesize": format.get("filesize")
                        })
            
                return video_formats

        except yt_dlp.utils.DownloadError as error:
            print("Donwload Error :",error)
            return []
    
        except Exception as error:
            print("Error while getting formats : ",error)
            return []
   
    #function for when browse folder to select donwload location
    def browse_folder(self):
        #show select folder dialog and get path of selected folder
        folder = QFileDialog.getExistingDirectory(self,"Select Donwload Folder")

        if folder:
            self.location_input.setText(folder)


       
    def resizeEvent(self, event):
        super().resizeEvent(event)
        if self.overlay:
            self.overlay.setGeometry(self.rect())
        
        if self.overlay2:
            self.overlay2.setGeometry(self.rect())

    #function to donwload selected formate
    def download(self):
        if getattr(self, "is_downloading", False):
            QMessageBox.warning(self, "Download in progress",
                            "Please wait until the current download finishes.")
            return
        self.on_radio_change()
        #get url
        url = self.url_input.text().strip()

        #saving location
        save_path = self.location_input.text().strip()

        if not url:
            QMessageBox.warning(self,"Warning","Please Enter URL")
            return 
        
        if not save_path:
            QMessageBox.warning(self,"Warning","Select Donwload Location")
            return 
        
      
      
        if self.video_radio.isChecked():
            isVideo = True
            format_info = self.quality_combobox.currentData()

        elif self.audio_radio.isChecked():
            isVideo = False
            format_info = (self.format_combobox.currentText() or "").strip().lower()
        
        self._max_percent = 0
        #create thread
        self.thread = QThread(self)
        #create worker object
        self.worker = DownloadWorker(url,save_path,format_info,isVideo)
        #move worker to the thread
        self.worker.moveToThread(self.thread)


        #connect signals
            #when thread started
        self.thread.started.connect(self.worker.run)
            #when thread emit progress signal
        self.worker.progress.connect(self.update_progress_bar)
            #when thread emit finished signal
        self.worker.finished.connect(self.worker_finished)
            #when thread emit error signal
        self.worker.error.connect(self.worker_error)

        
        #cleanup
            #when worker finish
        self.worker.finished.connect(self.thread.quit)
        self.worker.error.connect(self.thread.quit)
            #delete worker object
        self.worker.finished.connect(self.worker.deleteLater)
        self.worker.error.connect(self.worker.deleteLater)

        self.thread.finished.connect(self.thread.deleteLater)
 


        # reset flag when thread finishes
        self.thread.finished.connect(lambda: setattr(self, "is_downloading", False))

        # mark as downloading
        self.is_downloading = True
    
        #show progress bar
        self.download_progress.setValue(0)
        self.download_progress.show()
        self.progress_label.setText("-")
        self.progress_label.show()
        self.overlay2.show()
        self.overlay2.raise_()
        QApplication.processEvents()

        #start thread
        self.thread.start()

        #disable    
        self.download_button.setEnabled(False)

    #function for updating progress bar
    def update_progress_bar(self,percent,speed_str,eta_str):
        self.download_progress.setValue(percent)
        self.progress_label.setText(f"{speed_str} | {eta_str}")
        self._max_percent = max(self._max_percent, percent)
        self.download_progress.setValue(self._max_percent)

    def worker_finished(self,message):
        self.download_progress.hide()
        self.progress_label.hide()
        self.overlay2.hide()
        self.download_button.setEnabled(True)
        QMessageBox.information(self,"Success",message)
       
        
    def worker_error(self,errorMessage):
        self.download_progress.hide()
        self.progress_label.hide()
        self.overlay2.hide()
        self.download_button.setEnabled(True)
        QMessageBox.critical(self,"Error",errorMessage)
       

    #delete thread when app closed
    def closeEvent(self, e):
        if hasattr(self, "thread") and self.thread and self.thread.isRunning():
            self.worker.error.disconnect() if hasattr(self.worker, "error") else None
            self.thread.requestInterruption()  # optional if you implement it
            self.thread.quit()
            self.thread.wait()
            e.accept()

    #function when radio is selected
    def on_radio_change(self):     

        try:
            #get url 
            url = self.url_input.text().strip()

            #if no url found then return
            if not url:
                return


            #clear quality combobox
            self.quality_combobox.clear()

            #show loading
            self.overlay.show()
            self.overlay.raise_()

            QApplication.processEvents()  # force GUI update
            #get video and audio formats
            video_formats = self.get_format_of_video(url)

            self.overlay.hide()
            

            print(video_formats)
            if self.video_radio.isChecked():
                print("video")
                #hide formate field when video is selected
                self.format_label.setVisible(False)
                self.format_combobox.setVisible(False)
                #show quality field
                self.quality_label.setVisible(True)
                self.quality_combobox.setVisible(True)

                
                #loop through format and add items to quality combobox
                for format in (video_formats or []):
                    self.quality_combobox.addItem(f"{format['resolution']} ({format['ext']})",format["format_id"])

            elif self.audio_radio.isChecked():
                print("audio")
                #hide quality 
                self.quality_label.setVisible(False)
                self.quality_combobox.setVisible(False)
                #show formate
                self.format_label.setVisible(True)
                self.format_combobox.setVisible(True)

        except Exception as e:
            QMessageBox.critical(self,"Error","Unexpected Error")
            self.overlay.hide()

class DownloadWorker(QObject):

    #emit progress percent
    progress = pyqtSignal(int,str,str)
    #emit finshed signal
    finished = pyqtSignal(str)
    #emit if error
    error = pyqtSignal(str)

    def __init__(self,url,save_path,format_info,isVideo):
        super().__init__()
        self.url = url
        self.save_path = save_path
        self.format_info = format_info
        self.isVideo = isVideo
        

    
    def run(self):
        try:
            if self.isVideo:
                #create options for the ydl
                ydl_options = {
                    'outtmpl':f"{self.save_path}/%(title)s.%(ext)s",
                    'format':self.format_info,
                    'progress_hooks':[self.progress_hook],
                    'quiet':True,
                    'noprogress':True
                }

            elif not self.isVideo:
                #mp3 required postprocessor
                postprocessors = []

                if self.format_info != "original (best)":
                    postprocessors = [{
                        "key":"FFmpegExtractAudio",
                        "preferredcodec":self.format_info,
                        "preferredquality":"192"
                }]

                 #creating yt_dl options
                ydl_options = {
                    "format":"bestaudio/best",
                    "outtmpl":f"{self.save_path}/%(title)s.%(ext)s",
                    "noplaylist":True,
                    "postprocessors":postprocessors
                }

            #Call ydl api
            with yt_dlp.YoutubeDL(ydl_options) as ydl:
                #call download function written in the ydl object and pass url to download video
                ydl.download([self.url])
                self.finished.emit("Download Completed!")

        
        except DownloadError as e:
            self.error.emit(f"Download error: {str(e)}")
        except ExtractorError as e:
            self.error.emit(f"Extractor error: {str(e)}")
        except Exception as e:
            self.error.emit(f"Unexpected error: {str(e)}")
            
    
    def progress_hook(self,d):

        #if status is donwloading
        if d["status"] == 'downloading':
            #get total bytes to donwload
            total = d.get('total_bytes') or d.get('total_bytes_estimate')
            #get donwloaded bytes if there is no then store 0 
            downloaded = d.get('downloaded_bytes',0)

            #if total exist
            if total and downloaded:
                #calculate how many percent donwloaded
                percent = int(downloaded/total * 100)
                
                #donwload speed
                speed = d.get("speed") #bytes per second
                eta = d.get("eta")#second

                if speed:
                    speed_str = f"{speed/1024:.1f} KB/s"

                else:
                    speed_str = "-"

                if eta:
                    
                    #convert to the int
                    eta = int(float(eta))
                    
                    #format time
                    minutes,seconds = divmod(eta,60)
                    
                    if minutes:
                        eta_str = f"{minutes}m {seconds}s"

                    else:
                        eta_str = f"{seconds}s"
                else:
                    eta_str = ""
            

                #emit progress percentage
                self.progress.emit(percent,speed_str,eta_str)
            
        
        #if status is finished
        elif d['status'] == 'finished':
            self.progress.emit(100,"0 KB/s","0s remaining")




if __name__ == "__main__":
    app = QApplication([])
    main_window = App()
    main_window.show()
    app.exec_()