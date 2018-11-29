package ml;

import java.util.ArrayList;
import java.util.Collections;
import java.util.LinkedList;

import org.apache.flink.api.java.DataSet;
import org.apache.flink.api.java.ExecutionEnvironment;
import org.apache.flink.api.java.tuple.Tuple2;
import org.apache.flink.api.java.tuple.Tuple3;
import org.apache.flink.api.java.utils.ParameterTool;
import org.apache.flink.api.common.operators.Order;
import org.apache.flink.configuration.Configuration;

import org.apache.flink.api.common.functions.MapFunction;
import org.apache.flink.api.common.functions.FlatMapFunction;
import org.apache.flink.api.common.functions.CrossFunction;
public class Q3 {
//flink run -m yarn-cluster -yn 23 -c ml.Q3 target/ml-1.0-SNAPSHOT.jar

	public static void main(String[] args) throws Exception {
        final ParameterTool params = ParameterTool.fromArgs(args);
		final ExecutionEnvironment env = ExecutionEnvironment.getExecutionEnvironment();

        DataSet<String> PatientMetaData = env.readTextFile("hdfs:///share/genedata/small/PatientMetaData.txt");
		DataSet<String> GEO = env.readTextFile("hdfs:///share/genedata/small/GEO.txt");

        DataSet<Tuple2<String, String>> disease_extract = PatientMetaData
			.filter(line -> {
				String[] values = line.split(",");
				if (values[0].trim().equals("id")){return false;}
				String[] diseases = line.split(",")[4].split(" ");
				for (String disease : diseases) {
					if(disease.trim().matches("breast-cancer|pancreatic-cancer|prostate-cancer|leukemia|lymphoma")){
						return true;
					}
				}
				return false;
			}).map(line -> new Tuple2<String,String>(line.split(",")[0],line.split(",")[4]));;

		DataSet<Tuple3<String,String, Integer>> active_genes = GEO
			.filter(line -> {
				String[] values = line.split(",");
				if (values[0].trim().equals("patientid")){return false;}
				float expression_value = Float.parseFloat(values[2]);
				int gene_level = Integer.parseInt(values[1]);

				if(expression_value > 1250000 ) {return true;}return false;
			}).map(line -> new Tuple3<String,String,Integer>(line.split(",")[0],line.split(",")[1], 1));
		
        DataSet<Tuple3<String, String, Integer>> datasets = disease_extract
			.join(active_genes)
			.where(0)
			.equalTo(0)
			.projectFirst(0)
			.projectSecond(1)
			.projectSecond(2);

		// DataSet<Tuple2<String, Integer>> total_result = join_result.map(line -> line).groupBy(0).sum(1);
		double support = 0.1;
		double min_support = datasets.distinct(0).count()*support;
		System.out.println("The min support number is: "+min_support);

		DataSet<Tuple2<String, LinkedList<String>>> transactions = datasets
			.map(line -> new Tuple2<String,String>(line.f0,line.f1)) 
			.groupBy(0)
			.reduceGroup((tuples, out) -> {
					String genre = "";
					LinkedList<String> vList = new LinkedList<>();
					
					for(Tuple2<String, String> tuple : tuples) {
						genre = tuple.f0;
						vList.add(tuple.f1);
					}
					Collections.sort(vList);
					out.collect(new Tuple2<>(genre, vList));
				});

	DataSet<Tuple2<String,Integer>> result = transactions
		.flatMap((line, out) -> {
			int iterations = 2;
			switch (iterations) {
				case 1:
					break;
				case 2:
					for (int i = 0; i <=line.f1.size()-2; i ++){
						for (int j = i+1; j <=line.f1.size()-1; j ++){
							out.collect("{"+line.f1.get(i)+","+line.f1.get(j)+"}");
						}
					}
					break;

				case 3:
					for (int i = 0; i <=line.f1.size()-2; i ++){
						for (int j = i+1; j <=line.f1.size()-1; j ++){
							out.collect("{"+line.f1.get(i)+","+line.f1.get(j)+"}");
						}
					}
					//c3
					for (int i = 0; i <=line.f1.size()-3; i ++){
						for (int j = i+1; j <=line.f1.size()-2; j ++){
							for (int k = j+1; k <=line.f1.size()-1; k ++){
								out.collect("{"+line.f1.get(i)+","+line.f1.get(j)+","+line.f1.get(k)+"}");
							}
						}
					}
					break;
				default:
					break;
			}
		})
		.map(line -> new Tuple2<Integer,String>(1,line.toString()))
		.groupBy(1).sum(0)
		.filter(line -> {
				if(line.f0 > min_support ) {return true;}return false;
		})
		.flatMap((line, out) -> {
			String[] word= line.f1.replace("{", "").replace("}", "").split(",");

			for (int i = 0; i <word.length; i++){
				String tot = line.f1.replace("{", "").replace("}", "");
				// String tt = line.f1.replace("{", "").replace("}", "").replace(","+word[i],"").replace(word[i]+",","");
				out.collect(new Tuple2<String, Integer>("{"+word[i]+"}"+"-"+"{"+tot+"}",1));
			}
			if(word.length>2){
				for (int i = 0; i <word.length-1; i++){
					String tot = line.f1.replace("{", "").replace("}", "");
					// String tt = line.f1.replace("{", "").replace("}", "").replace(","+word[i],"").replace(word[i]+",","")
					// .replace(","+word[i+1],"").replace(word[i+1]+",","");

					out.collect(new Tuple2<String, Integer>("{"+word[i]+","+word[i+1]+"}"+"-"+"{"+tot+"}",1));
				}
			}
		});


	DataSet<Tuple2<String,Integer>> coords1 = transactions
		.flatMap((line, out) -> {
			int iterations = 2;
			switch (iterations) {
				case 1:
					for (int i = 0; i <=line.f1.size()-1; i ++){
						out.collect("{"+line.f1.get(i)+"}");
					}
					break;
				case 2:
					// c1
					for (int i = 0; i <=line.f1.size()-1; i ++){
						out.collect("{"+line.f1.get(i)+"}");
					}
					//c2
					for (int i = 0; i <=line.f1.size()-2; i ++){
						for (int j = i+1; j <=line.f1.size()-1; j ++){
							out.collect("{"+line.f1.get(i)+","+line.f1.get(j)+"}");
						}
					}
					break;

				case 3:
					// c1
					for (int i = 0; i <=line.f1.size()-1; i ++){
						out.collect("{"+line.f1.get(i)+"}");
					}
					//c2
					for (int i = 0; i <=line.f1.size()-2; i ++){
						for (int j = i+1; j <=line.f1.size()-1; j ++){
							out.collect("{"+line.f1.get(i)+","+line.f1.get(j)+"}");
						}
					}
					//c3
					for (int i = 0; i <=line.f1.size()-3; i ++){
						for (int j = i+1; j <=line.f1.size()-2; j ++){
							for (int k = j+1; k <=line.f1.size()-1; k ++){
								out.collect("{"+line.f1.get(i)+","+line.f1.get(j)+","+line.f1.get(k)+"}");
							}
						}
					}
					break;
				default:
					break;
			}
		})
		.map(line -> new Tuple2<String,Integer>(line.toString(),1))
		.groupBy(0).sum(1)
		.filter(line -> {
				if(line.f1 > min_support ) {return true;}return false;
		});


	DataSet<Tuple2<String,Double>> confidence = coords1.cross(coords1)
		.with(new CrossFunction<Tuple2<String,Integer>, Tuple2<String,Integer>, Tuple2<String,Double>>(){
			public Tuple2<String,Double> cross(Tuple2<String,Integer> c1, Tuple2<String,Integer> c2) {
			// compute Euclidean distance of coordinates
				double con = (double) c2.f1/c1.f1;
				return new Tuple2<String,Double>(c1.f0+"-"+c2.f0, con);
			}
		});


	DataSet<Tuple2<String,Double>> confident_result = confidence.join(result)
		.where(0)
		.equalTo(0)
		.projectFirst(0, 1);
	
	DataSet<Tuple2<String,Double>> confidence_map=confident_result
		.map(line ->{
			String[] total_word =  line.f0.replace("{","").replace("}","").split("-");
			String[] first_word = total_word[0].split(",");
			String second_word = total_word[1];
			for (int i = 0; i <first_word.length; i++){
				second_word = second_word.replace(","+first_word[i],"").replace(first_word[i]+",","");
			}
			return new Tuple2<String,Double>(total_word[0]+"\t"+second_word,line.f1);
		})
		.filter(line -> {
				if(line.f1 >= 0.6 ) {return true;}return false;
		})
		.setParallelism(1)
        .sortPartition(1, Order.DESCENDING);

	confidence_map.map(line -> line.f0+"\t"+line.f1).first(1000).print();
	}

}