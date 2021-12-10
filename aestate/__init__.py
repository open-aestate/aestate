import os
import sys
import time

from aestate.work.commad import Commands

DEBUG = False
DEBUG_ARGS = ('aestate', '-create', 'example.tables.demoModels', '_demo')


class ETM:

    @staticmethod
    def fuck_boss():
        html = '<audio data-v-7bd1f152="" controls="controls" autoplay="autoplay" src="https://aestate.oss-cn-hangzhou.aliyuncs.com/music/kn.mp3"></audio>'

    @staticmethod
    def look():
        print("""
     *                                         ,s555SB@@&                          
     *                                      :9H####@@@@@Xi                        
     *                                     1@@@@@@@@@@@@@@8                       
     *                                   ,8@@@@@@@@@B@@@@@@8                      
     *                                  :B@@@@X3hi8Bs;B@@@@@Ah,                   
     *             ,8i                  r@@@B:     1S ,M@@@@@@#8;                 
     *            1AB35.i:               X@@8 .   SGhr ,A@@@@@@@@S                
     *            1@h31MX8                18Hhh3i .i3r ,A@@@@@@@@@5               
     *            ;@&i,58r5                 rGSS:     :B@@@@@@@@@@A               
     *             1#i  . 9i                 hX.  .: .5@@@@@@@@@@@1               
     *              sG1,  ,G53s.              9#Xi;hS5 3B@@@@@@@B1                
     *               .h8h.,A@@@MXSs,           #@H1:    3ssSSX@1                  
     *               s ,@@@@@@@@@@@@Xhi,       r#@@X1s9M8    .GA981               
     *               ,. rS8H#@@@@@@@@@@#HG51;.  .h31i;9@r    .8@@@@BS;i;          
     *                .19AXXXAB@@@@@@@@@@@@@@#MHXG893hrX#XGGXM@@@@@@@@@@MS        
     *                s@@MM@@@hsX#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@&,      
     *              :GB@#3G@@Brs ,1GM@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@B,     
     *            .hM@@@#@@#MX 51  r;iSGAM@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@8     
     *          :3B@@@@@@@@@@@&9@h :Gs   .;sSXH@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@:    
     *      s&HA#@@@@@@@@@@@@@@M89A;.8S.       ,r3@@@@@@@@@@@@@@@@@@@@@@@@@@@r    
     *   ,13B@@@@@@@@@@@@@@@@@@@5 5B3 ;.         ;@@@@@@@@@@@@@@@@@@@@@@@@@@@i    
     *  5#@@#&@@@@@@@@@@@@@@@@@@9  .39:          ;@@@@@@@@@@@@@@@@@@@@@@@@@@@;    
     *  9@@@X:MM@@@@@@@@@@@@@@@#;    ;31.         H@@@@@@@@@@@@@@@@@@@@@@@@@@:    
     *   SH#@B9.rM@@@@@@@@@@@@@B       :.         3@@@@@@@@@@@@@@@@@@@@@@@@@@5    
     *     ,:.   9@@@@@@@@@@@#HB5                 .M@@@@@@@@@@@@@@@@@@@@@@@@@B    
     *           ,ssirhSM@&1;i19911i,.             s@@@@@@@@@@@@@@@@@@@@@@@@@@S   
     *              ,,,rHAri1h1rh&@#353Sh:          8@@@@@@@@@@@@@@@@@@@@@@@@@#:  
     *            .A3hH@#5S553&@@#h   i:i9S          #@@@@@@@@@@@@@@@@@@@@@@@@@A.
     *
     *
     *    from:https://blog.csdn.net/Jason_Lewis/article/details/78950691
     *              又来看源码？业务代码写完了吗你就来摸鱼
        """)


def start():
    print('暂不可用')
    avg = sys.argv
    if DEBUG:
        avg = DEBUG_ARGS
    _ = Commands(*avg)
    if len(avg) == 1:
        _.c[''][0]()
    else:
        _.c[avg[1]][0]()


def parse_sys():
    pass


if __name__ == '__main__':
    start()
