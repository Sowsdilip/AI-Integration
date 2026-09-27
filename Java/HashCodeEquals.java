package com.cs.pratice;

import java.util.HashMap;
import java.util.Map;

public class HashCodeEquals {

	public static void main(String[] args) {
		Ticket t1 = new Ticket("Sowmya");
		Ticket t2 = new Ticket("Sowmya");

		Map<Ticket, String> testMap = new HashMap<>();
		testMap.put(t1, "urgent");
		
		System.out.println(testMap.get(t2));
	}

}
