/*
 * OpenCV video streaming over TCP/IP
 * Client: Receives video from server and display it
 *
 */

#include "opencv2/opencv.hpp"

#include "opencv2/highgui.hpp"
#include "opencv2/imgproc.hpp"
#include "opencv2/core.hpp"

#include <sys/socket.h> 
#include <arpa/inet.h>
#include <unistd.h>

using namespace cv;

int QUIT = 1;

Mat imgImporvement(Mat src);

int main(int argc, char** argv)
{
    //--------------------------------------------------------
    //networking stuff: socket , connect
    //--------------------------------------------------------
    int         socket_fd;
    char*       serverIP;
    int         serverPort;

    if (argc < 3) {
           std::cerr << "Usage: cv_video_cli <serverIP> <serverPort> " << std::endl;
    }

    serverIP   = argv[1];
    serverPort = atoi(argv[2]);

    struct  sockaddr_in serverAddr;
    socklen_t           addrLen = sizeof(struct sockaddr_in);

    if ((socket_fd = socket(PF_INET, SOCK_STREAM, 0)) < 0) {
        std::cerr << "socket() failed" << std::endl;
    }

    serverAddr.sin_family = PF_INET;
    serverAddr.sin_addr.s_addr = inet_addr(serverIP);
    serverAddr.sin_port = htons(serverPort);

    if (connect(socket_fd, (sockaddr*)&serverAddr, addrLen) < 0) {
        std::cerr << "connect() failed!" << std::endl;
    }

    //----------------------------------------------------------
    //OpenCV Code
    //----------------------------------------------------------

    Mat img;
    img = Mat::zeros(480 , 640, CV_8UC3);
    int imgSize = img.total() * img.elemSize();
    uchar *iptr = img.data;
    int bytes = 0;
    int key;

    //make img continuos
    if ( ! img.isContinuous() ) { 
        img = img.clone();
    }
        
    std::cout << "Image Size:" << imgSize << std::endl;

    namedWindow("CV Video Client", 1);

    clock_t last_cycle = clock();
    while (key != 'q') {
        if ((bytes = recv(socket_fd, iptr, imgSize , MSG_WAITALL)) == -1) {
            std::cerr << "recv failed, received bytes = " << bytes << std::endl;
        }
        img = imgImporvement(img);
        cv::imshow("CV Video Client", img);
        clock_t next_cycle = clock();
        double duration = (next_cycle - last_cycle) / (double) CLOCKS_PER_SEC;
        std::cout << "\tFPS:" << (1 / duration) << std::endl;
        std::cout << next_cycle - last_cycle;
        last_cycle = next_cycle;
        if (key = cv::waitKey(10) >= 0) break;
    }

    // tell server to quit
    send(socket_fd, (void *)QUIT, sizeof(QUIT), 0);

    close(socket_fd);

    return 0;
}

Mat imgImporvement(Mat src){

        //----------------------------------- Anti-glare ---------------------------
        Mat img( src.size() , src.type() );

        src.copyTo(img);

        Mat lab,
            lab_planes[3],
            clahe_bgr,
            grayimg,
            mask,
            result;

        Ptr<CLAHE> vClahe;

        cvtColor( img , lab , COLOR_BGR2Lab );

        split(lab, lab_planes);

        vClahe = createCLAHE(2.0);

        vClahe->apply(lab_planes[0],lab_planes[0]);

        merge(lab_planes,3,lab);

        cvtColor(lab, clahe_bgr, COLOR_Lab2BGR);

        cvtColor(clahe_bgr, grayimg, COLOR_BGR2GRAY);

        threshold(grayimg, mask, 220, 255, THRESH_BINARY);

        inpaint(img, mask, result, 21, INPAINT_TELEA);
        
        /*
        Mat grayimg,
            mask,
            result;

        cvtColor(img, grayimg, COLOR_BGR2GRAY);

        threshold(grayimg, mask, 220, 255, THRESH_BINARY);

        inpaint(img, mask, result, 21, INPAINT_TELEA);
        */

        //----------------------------------- Anti-shake ---------------------------
        


        return result;

}
