package com.example.demo;

import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.Future;

public class ThreadPoolTiming {
	
	static void run(String label,ExecutorService execute) throws InterruptedException, ExecutionException {
		long start = System.nanoTime();
		List<Future<String>> futures = new ArrayList<>();
		for(int i=1;i<=2000;i++){
			int id = 1;
			futures.add(execute.submit(()->{
				Thread.sleep(1000);
				return "task "+id+" on "+Thread.currentThread();
			}));
		}
        for(Future<String> f:futures)
        	System.out.println(f.get());
        execute.shutdown();
        System.out.printf("%s: %.1fs%n%n", label, (System.nanoTime() - start) / 1e9);	
	}

	public static void main(String[] args) throws Exception {
        //run("fixed pool (1 thread, control)", Executors.newFixedThreadPool(1)); // ~10s
        run("fixed pool (2 threads)", Executors.newFixedThreadPool(100));         // ~5s
        run("virtual threads", Executors.newVirtualThreadPerTaskExecutor());    // ~5s
    }
}
