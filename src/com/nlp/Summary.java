package com.nlp;

import static spark.Spark.*;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.List;
import javax.json.*;

import spark.Spark;

public class Summary {

		
	    public static void main(String[] args) {
	    	
	    	Spark.staticFileLocation("com/nlp/public");
	    	
	    	
	    	
	        get("/invokeTFIDF", (req, res) -> {
	        	
	        	// Process p = Runtime.getRuntime().exec("dir"); 
	        	 Process p = Runtime.getRuntime().exec("python tf_idf.py"); 
	        	/*BufferedReader br = new BufferedReader(new InputStreamReader(p.getInputStream()));
	 	        String s = br.readLine(); 
	 	        System.out.println(s);
	 	        System.out.println("Sent");
	 	        try{
	 	        p.waitFor();
	 	        }catch (Exception e) {
					// TODO: handle exception
	 	        	System.out.println(e.getMessage());
				}
	 	        
	 	        p.destroy();
	 	        */
	 	       
	 	       
	        	return "Success";
	        });
	        
	        
 get("/invokeGSS", (req, res) -> {
	        	
	        	// Process p = Runtime.getRuntime().exec("dir"); 
	        	 Process p = Runtime.getRuntime().exec("python compute_gss.py"); 
	        	/*BufferedReader br = new BufferedReader(new InputStreamReader(p.getInputStream()));
	 	        String s = br.readLine(); 
	 	        System.out.println(s);
	 	        System.out.println("Sent");
	 	        try{
	 	        p.waitFor();
	 	        }catch (Exception e) {
					// TODO: handle exception
	 	        	System.out.println(e.getMessage());
				}
	 	        
	 	        p.destroy();
	 	        */
	 	       
	 	       
	        	return "Success";
	        });
 
 get("/getGSSprogress", (req, res) -> {
	 String sCurrentLine = null;
	 StringBuilder str = new StringBuilder();
 	
	 try (BufferedReader br = new BufferedReader(new FileReader("gssprogress.txt"))) {

			

			while ((sCurrentLine = br.readLine()) != null) {
				System.out.println(sCurrentLine);
				str.append(sCurrentLine);
			}

		} catch (IOException e) {
			e.printStackTrace();
		}
     
     
 	return "{ \"progress\":"+str.toString()+"}";
 });
 
 
 
 get("/getGSSdetails", (req, res) -> {
	 	
	 String sCurrentLine=null;
	 StringBuilder str = new StringBuilder();
	 	try (BufferedReader br = new BufferedReader(new FileReader("gssdetails.txt"))) {

				

				while ((sCurrentLine = br.readLine()) != null) {
					System.out.println(sCurrentLine);
					str.append(sCurrentLine);
				}

			} catch (IOException e) {
				e.printStackTrace();
			}
	     
	     
	 	return str.toString();
	 });
 
 get("/getTFIDFprogress", (req, res) -> {
	 
	 String sCurrentLine=null;
	 StringBuilder str = new StringBuilder();
	 
		 try (BufferedReader br = new BufferedReader(new FileReader("progress.txt"))) {

				

				while ((sCurrentLine = br.readLine()) != null) {
					//System.out.println(sCurrentLine);
					str.append(sCurrentLine);
				}

			} catch (IOException e) {
				e.printStackTrace();
			}
	     
	     
		 return "{ \"progress\":"+str.toString()+"}";
	 });
 
get("/getTFIDFdetails", (req, res) -> {
	 
	 String sCurrentLine=null;
	 StringBuilder str = new StringBuilder();
	 List<String> list = new ArrayList<String>();
	 
	 
		 try (BufferedReader br = new BufferedReader(new FileReader("tfidfdetails.txt"))) {

				

				while ((sCurrentLine = br.readLine()) != null) {
					//System.out.println(sCurrentLine);
					str.append(sCurrentLine);
				}

			} catch (IOException e) {
				e.printStackTrace();
			}
		 
		
	     
	    // System.out.println(list.toString());
		 return str.toString();
	 });
	       

get("/getsummary", (req, res) -> {
	 
	 String sCurrentLine=null;
	 StringBuilder str = new StringBuilder();
	 List<String> list = new ArrayList<String>();
	 
	 
		 try (BufferedReader br = new BufferedReader(new FileReader("summaryjson.txt"))) {

				

				while ((sCurrentLine = br.readLine()) != null) {
					//System.out.println(sCurrentLine);
					str.append(sCurrentLine);
				}

			} catch (IOException e) {
				e.printStackTrace();
			}
		 
	     
	    // System.out.println(list.toString());
		 return str.toString();
	 });
	      
	    }
	
	
	
}
