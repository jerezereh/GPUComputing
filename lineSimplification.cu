#include <iostream>
#include <sstream>
#include <fstream>
#include <vector>
#include <string>

/**
 * Input: trajectory of points, in order from first to last, list of points that cannot be simplified out
 * Output: list of simplified points
 */


__global__ void lsKernel(int* pointData, int arraySize) {
    
}

int myRandInt() {
    int num = rand() % 100 +1;
    if( rand( ) % 2 == 0 )
        num *= -1;
    return num;
}

int main(int argc, char * argv[]) {
    if (argc != 3) {
        cout << "Program requires 3 arguments: [exe] [trajectory] [point list]\n";
    }
    else {
        
    }
    

    // Create an array of numbers in traditional memory.
    // Fill the array with random values
    std::vector<int> data;
    srand(0);
    for( int i = 0; i < total; i++ )
    {
        int tmp = myRandInt( );
        data.push_back( tmp );
    }

    // Step 1:  Create an array on the GPU to hold the numbers that we
    // will do the sum3 computation on
    int *device_nums;
    cudaMalloc( &device_nums, data.size() * sizeof( int) );

    // Step 2: Copy the data to the device array
    cudaMemcpy(device_nums, &(data[0]), data.size() * sizeof( int), cudaMemcpyHostToDevice);

    //Step 3:  We must keep track of the number of triples that sum
    // to 0.  We will create a single memory location (variable) on
    // the GPU that is SHARED among ALL threads.  Whenever a thread
    // finds a triple that sums to 0, this variable will be incremented
    int* device_count;
    cudaMalloc( &device_count, sizeof( int) );
    {
        // initialize the count to 0
        int startCount = 0;
        cudaMemcpy(device_count, &(startCount), sizeof( int), cudaMemcpyHostToDevice);
    }


    // Just some code to time the kernel
    cudaEvent_t startTotal, stopTotal;
    float timeTotal;
    cudaEventCreate(&startTotal);
    cudaEventCreate(&stopTotal);
    cudaEventRecord( startTotal, 0 );



    // Step 4:  Decide how many threads we will organize into a block.  The
    // number of threads required will depend on the length of the array
    // containing random numbers.  Here, we are simply figuring out
    // how many threads we need based on the size of that array
    // (we allocated the array as an STL vector)
    //
    // Since EACH thread gets 2 fixed values, we are going to give threads
    // ID numbers that will indicate the array indexes of the 3 values
    // that will be fixed in that thread.  So, we create a 2 dimensional
    // thread block.  It simply labels each thread with 2 numbers that form
    // its identifier.
    dim3 threadsPerBlock(16,32);
    dim3 numBlocks((data.size() +threadsPerBlock.x-1)/ threadsPerBlock.x,
            (data.size() +threadsPerBlock.y-1)/ threadsPerBlock.y);

    std::cerr <<"data size: " <<(data.size()) << std::endl;
    std::cerr <<"block sizes: " <<(data.size() +threadsPerBlock.x-1)/ threadsPerBlock.x
        <<", " <<(data.size() +threadsPerBlock.y-1)/ threadsPerBlock.y <<  std::endl;


    // Step 5.  Now we have computed how many threads to launch.  We have
    // given each thread and identifier consisting of a pair (x,y).
    // Finally, launch the threads.
    sum3Kernel<<< numBlocks, threadsPerBlock>>> ( device_nums, data.size(), device_count );


    // Step 6:  After the threads have all finished, the count of triples that
    // sum to 0 is still stored on the GPU.  We just need to transfer it
    // back to the CPU so we can print it out.
    int totalFound;
    cudaMemcpy(&totalFound, device_count, sizeof( int), cudaMemcpyDeviceToHost);

    // stop the timer
    cudaEventRecord( stopTotal, 0 );
    cudaEventSynchronize( stopTotal );
    cudaEventElapsedTime( &timeTotal, startTotal, stopTotal );
    cudaEventDestroy( startTotal );
    cudaEventDestroy( stopTotal );

    // print it out!
    std::cerr << "total time in seconds: " << timeTotal / 1000.0 << std::endl;
    std::cerr << "Total triples found: " << totalFound  <<std::endl;
}