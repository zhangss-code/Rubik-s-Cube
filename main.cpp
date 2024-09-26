#include <iostream>
#include <opencv2/opencv.hpp>

using namespace std;
using namespace cv;
void  imageread(char path[50]);//测试
void Read_Space_BGR(int x,int y,int weight,int height);//读取bgr
void Simple_Set();//对魔方的标准色块获取


//定义全局mat图像
Mat Global_Image;
//定义全局的vec3b
Vec3b BGR_g;
//设置魔方每个色块标准bgr
            struct BGR_SIMPLE
            {
                int BGR_SIMPLE_0[255][255][255];
            };
            struct BGR_SIMPLE bgr1_white,bgr2_blue,bgr3_yellow,bgr4_red,bgr5_green,bgr6_orange;

int main() {
    /**  // 指定图片路径
    string path = "panda.png";
    cv::Mat img = imread(path);  // 读取图像 */
  //imageread("/home/zhangshunshun/png/1.jpeg");
  Global_Image = imread("/home/zhangshunshun/1.jpg");
int x,y;
cin>>x;
cin>>y;




   Read_Space_BGR(x,y,20,20);//x,y,weight,height

    
    return 0;
}

//读取照片并显示
void imageread(char path[50])
{
    
    Global_Image =  imread(path);//路径和加载方式（可选）
 
    if(Global_Image.empty())
    {
        printf("error open png");
 
    }
    //namedWindow("input",参数);//自己选择图像窗口，没有则永远保持原大小
    namedWindow("Display Image", WINDOW_AUTOSIZE );
    imshow("input",Global_Image);

    waitKey(0);    //停止，保持图片显示

    destroyAllWindows();

}
//读取照片指定地方的bgr 保存在BGR_g
void Read_Space_BGR(int x,int y,int weight,int height)
{
  

    Rect roi(x,y,weight,height);  //x,y,weight,height

    Mat region = Global_Image(roi);

    //显示一下
    imshow("input",region);
    waitKey(0);

    

    destroyAllWindows();
    //读取BGR
    int b=0,g=0,r=0;
    for (int y=0;y<region.rows;y++)
    {
        for (int x = 0; x< region.cols; x++)

        {
            /* code */
           BGR_g = region.at<Vec3b>(y,x);//将全局BGR读取,好像不用全局的BGR
              //求平均bgr
             
             b += BGR_g[0];
           
             g+=BGR_g[1];
           
             r+=BGR_g[2];

             



        }
        
        
        

        


    }

short int  b1 =b/(region.rows*region.cols);
short int  g1 =g/(region.rows*region.cols);
short int  r1 =r/(region.rows*region.cols);

cout<<b<<" :"<<b1<<" "<<endl;
cout<<g<<" :"<<g1<<" "<<endl;
cout<<r<<" :"<<r1<<" "<<endl;

Mat BGR_SHOW = Mat::zeros(100,100,CV_16F);
Vec3b BGRColor=(b1,g1,r1);
 for (int y=0;y<100;y++)
    {
        for (int x = 0; x< 100; x++)

        {
            /* code */
           BGR_SHOW.at<Vec3b>(y,x)=BGRColor;//将全局BGR读取,好像不用全局的BGR
             

        }
    }
imshow("test",BGR_SHOW);
waitKey(0);
destroyAllWindows();



    


}
  void Simple_Set() //对魔方的标准色块获取

    {
       

    }
