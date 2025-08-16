#Import modules
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication,QWidget,QVBoxLayout,QHBoxLayout,QLabel,QPushButton,QLineEdit,QComboBox,QRadioButton,QButtonGroup,QProgressBar

class App(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("YouTube Downloader")
        self.resize(500,350)

        self.master_layout = QVBoxLayout()

        #creating labels
        self.url_label = QLabel("Video URL :")
        self.type_label = QLabel("Type :")
        self.format_label = QLabel("Format :")
        self.quality_label = QLabel("Quality :")
        self.location_label = QLabel("Location :")
        self.progress_label = QLabel("")

        #creating buttons
        self.browse_button = QPushButton("Browse")
        self.download_button = QPushButton("Download")
        
        #creating text input
        self.url_input = QLineEdit()
        self.location_input = QLineEdit()
        
        #creating combobox
        self.format_combobox = QComboBox()
        self.quality_combobox = QComboBox()
        
            #audio formates
        audioFormats = ["Original (Best)","MP3","AAC","WAV","FLAC","OGG"]

            #adding formates
        self.format_combobox.addItems(audioFormats)


        #Radio Buttons
        self.video_radio = QRadioButton("Video")
        self.audio_radio = QRadioButton("Audio")

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
        self.url_row = QHBoxLayout()
        self.url_row.addWidget(self.url_label)
        self.url_row.addWidget(self.url_input)

            #type
        self.type_row = QHBoxLayout()
        self.type_row.addWidget(self.type_label)
        self.type_row.addWidget(self.video_radio)
        self.type_row.addWidget(self.audio_radio)


            #Quality
        self.quality_row = QHBoxLayout()
        self.quality_row.addWidget(self.quality_label)

            #format
        self.format_row = QHBoxLayout()
        self.format_row.addWidget(self.format_label)
        self.format_row.addWidget(self.format_combobox)

            #location
        self.location_row = QHBoxLayout()
        self.location_row.addWidget(self.location_label)
        self.location_row.addWidget(self.location_input)
        self.location_row.addWidget(self.browse_button)

            #download
        self.download_row = QHBoxLayout()
        self.download_row.addWidget(self.download_button)

            #progressbar
        self.progress_row = QHBoxLayout()
        self.progress_row.addWidget(self.download_progress)
        self.progress_row.addWidget(self.progress_label)
        

        #adding all layout to master layout
        self.master_layout.addLayout(self.url_row)
        self.master_layout.addLayout(self.type_row)
        self.master_layout.addLayout(self.format_row)
        self.master_layout.addLayout(self.quality_row)
        self.master_layout.addLayout(self.location_row)
        self.master_layout.addLayout(self.download_row)
        self.master_layout.addLayout(self.progress_row)

        #set to main layout
        self.setLayout(self.master_layout) 


        #adding style
        self.setStyleSheet(""" 
            QWidget{
                background-color:#121212;
                color:#ffffff;
                font-family:Arial;
                font-size:14px;
                padding-left:10px;
                padding-right:20px;              
            }
            QLabels{
                font-size:16px;
                margin-bottom:10px;
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
            QPushButton {
                background-color: #1db954;
                color: white;
                border-radius: 8px;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background-color: #1ed760;
            }
            QPushButton:pressed {
                background-color: #1aa34a;
            }
        """)





if __name__ == "__main__":
    app = QApplication([])
    main_window = App()
    main_window.show()
    app.exec_()