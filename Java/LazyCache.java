package com.example.demo;

import java.util.*;
import java.util.concurrent.*;
import java.util.concurrent.atomic.AtomicInteger;

public class LazyCache {
    static final AtomicInteger loadCount = new AtomicInteger();

   // private volatile Map<String, String> data;   // volatile is essential
    private static Map<String, String> data; 
    
    static {
    	 data = load();
    }

    private static Map<String, String> load() {
        loadCount.incrementAndGet();
        try { Thread.sleep(5000); } catch (InterruptedException e) { Thread.currentThread().interrupt(); }
        return Map.copyOf(Map.of("a", "1", "b", "2"));  // immutable
    }

    public Map<String, String> get() {
        Map<String, String> local = data;   
        System.out.println("local data "+local);
        // 1st check, no lock (fast path)
        if (local == null) {
           /// synchronized (this) {
                local = data;                      // 2nd check, under lock
            //    if (local == null) {
                    local = load();
                    data = local;  
                    System.out.println("after loading local data "+data);// safe publication via volatile write
            //    }
           // }
        }
        return local;
    }

    public static void main(String[] args) throws Exception {
        LazyCache cache = new LazyCache();
        int n = 50;
        CountDownLatch ready = new CountDownLatch(n), go = new CountDownLatch(1);
        try (var exec = Executors.newVirtualThreadPerTaskExecutor()) {
            for (int i = 0; i < n; i++) {
                exec.submit(() -> {
                    ready.countDown();
                    go.await();                    // release all threads at once
                    cache.get();
                    return null;
                });
            }
            ready.await();
            go.countDown();
        }
        System.out.println("load() called " + loadCount.get() + " time(s)");  // expect 1
    }
}
