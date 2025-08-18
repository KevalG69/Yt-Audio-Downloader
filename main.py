#Import modules
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication,QWidget,QFormLayout,QVBoxLayout,QHBoxLayout,QLabel,QPushButton,QLineEdit,QComboBox,QRadioButton,QButtonGroup,QProgressBar
from PyQt5.QtWidgets import QFileDialog,QMessageBox
from PyQt5.QtGui import QPixmap
import yt_dlp

class App(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("ytDownloader By KevalG69")
        self.resize(500,250)

        self.master_layout = QVBoxLayout()
        #loader

            #creating overlay to cover whole window
        self.overlay = QWidget(self)
            #setting style
        self.overlay.setStyleSheet("background-color: rgba(0, 0, 0, 190); font-weight:bold;")

            #cover whole window
      
            #block other input
        self.overlay.setAttribute(Qt.WA_TransparentForMouseEvents,False)

            #inside overlay
        self.layout = QVBoxLayout(self.overlay)
        self.layout.setAlignment(Qt.AlignCenter)

        self.loader_label = QLabel()
        self.loader_text = QLabel("Wait while we are stealing from the cloud...")
        self.loader_label.setAlignment(Qt.AlignCenter)
        self.loader_text.setAlignment(Qt.AlignCenter)
    
            #setting gif in the loader label
        self.pixmap = QPixmap("waiting.jpg")
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
        self.progress_row = QHBoxLayout()
        self.progress_row.addStretch(1)
        self.progress_row.addWidget(self.download_progress)
        self.progress_row.addWidget(self.progress_label)
        
        self.download_progress.setMinimumWidth(468)
        self.progress_row.addStretch(1)

        self.download_progress.setVisible(False)
        self.progress_label.setVisible(False)

        self.form_layout.addRow(self.progress_row)        

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


    #progress bar function
    def progress_hook(self,d):
        
        if d["status"] == "downloading":
            total = d.get('total_bytes') or d.get('total_bytes_estimate')
            downloaded = d.get("downloaded_bytes",0)
            
            if total:
                self.download_progress.setVisible(True)
                self.progress_label.setVisible(True)
                percent = int(downloaded/total*100)
                self.download_progress.setValue(percent)
                self.progress_label.setText(f"{percent}%")
        elif d["status"] == "finished":
            self.download_progress.setValue(100)
            self.progress_label.setText("Completed!")
    def resizeEvent(self, event):
        super().resizeEvent(event)
        if self.overlay:
            self.overlay.setGeometry(self.rect())

    #function to donwload selected formate
    def download(self):


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
        

        self.overlay.show()
        self.overlay.raise_()
        QApplication.processEvents()
        #download video if selected
        if self.video_radio.isChecked():

            #get formate id
            format_id = self.quality_combobox.currentData()
            #create yt_dl options
            ydl_options = {
                "format":format_id,
                "outtmpl":f"{save_path}/%(title)s.%(ext)s",
                "noplaylist":True
            }

        elif self.audio_radio.isChecked():
            #get audio format selected
            audio_format = self.format_combobox.currentText().lower()

            #mp3 requires postprocessors
            postprocessors = []

            if audio_format != "original (best)":
                postprocessors = [{
                    "key":"FFmpegExtractAudio",
                    "preferredcodec":audio_format,
                    "preferredquality":"192"
                }]


            #creating yt_dl options
            ydl_options = {
                "format":"bestaudio/best",
                "outtmpl":f"{save_path}/%(title)s.%(ext)s",
                "noplaylist":True,
                "postprocessors":postprocessors
            }

        try:
           
            with yt_dlp.YoutubeDL(ydl_options) as ydl:
                self.download_button.setEnabled(False)
                ydl.download([url])
                self.overlay.hide()
                
                QMessageBox.information(self,"Success","Donwload Completed")
        
        except Exception as error:
            self.loader_label.hide()
            QMessageBox.critical(self,"Error",f"Failed to donwload:\n{str(error)}")

        finally:
            self.download_button.setEnabled(True)

           
       

    #function when radio is selected
    def on_radio_change(self):     
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
            for format in video_formats:
                self.quality_combobox.addItem(f"{format['resolution']} ({format['ext']})",format["format_id"])

        elif self.audio_radio.isChecked():
            print("audio")
            #hide quality 
            self.quality_label.setVisible(False)
            self.quality_combobox.setVisible(False)
            #show formate
            self.format_label.setVisible(True)
            self.format_combobox.setVisible(True)


    

    


if __name__ == "__main__":
    app = QApplication([])
    main_window = App()
    main_window.show()
    app.exec_()