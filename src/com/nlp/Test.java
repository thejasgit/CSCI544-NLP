package com.nlp;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Test {

	
	public static void main(String[] args) throws IOException {
		String [] cmd={"python", "/c", "C:\\Users\\Thejas\\workspace\\SummaryGenerator\\src\\com\\nlp\\temp.py"};
		
		 Process p = Runtime.getRuntime().exec("python tf_idf.py"); 
	        BufferedReader br = new BufferedReader(new InputStreamReader(p.getInputStream()));
	        System.out.println("Working Directory = " +
	                System.getProperty("user.dir"));
	        try {
				p.waitFor();
			} catch (InterruptedException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
	        String s =null;
	        while((s = br.readLine())!=null){
	        	 System.out.println(s);	
	        }
	        
	       // s = br.readLine(); 
	      //  System.out.println(s);
	        System.out.println("Sent");
	        p.destroy();
	       
	        
	       
	}
}
