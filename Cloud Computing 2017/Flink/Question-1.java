package ml;

import java.util.Collections;
import java.util.LinkedList;

import org.apache.flink.api.common.operators.Order;
import org.apache.flink.api.java.DataSet;
import org.apache.flink.api.java.ExecutionEnvironment;
import org.apache.flink.api.java.tuple.Tuple2;
import org.apache.flink.api.java.tuple.Tuple3;
import org.apache.flink.api.java.utils.ParameterTool;

public class Q1 {
//flink run -m yarn-cluster -yn 3 -c ml.Q1 target/ml-1.0-SNAPSHOT.jar

	public static void main(String[] args) throws Exception {
        final ParameterTool params = ParameterTool.fromArgs(args);
		final ExecutionEnvironment env = ExecutionEnvironment.getExecutionEnvironment();

        DataSet<String> PatientMetaData = env.readTextFile("hdfs:///share/genedata/large/PatientMetaData.txt");
		DataSet<String> GEO = env.readTextFile("hdfs:///share/genedata/large/GEO.txt");


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
			}).flatMap((line, out) -> {
			String[] diseases = line.split(",")[4].split(" ");
			for (String disease : diseases) {
				if(disease.trim().matches("breast-cancer|pancreatic-cancer|prostate-cancer|leukemia|lymphoma")){
					out.collect(new Tuple2<String, String>(line.split(",")[0], disease));
				}
			}});

		DataSet<Tuple2<String, Integer>> active_genes = GEO
			.filter(line -> {
					String[] values = line.split(",");
					if (values[0].trim().equals("patientid")){return false;}
					float expression_value = Float.parseFloat(values[2]);
					int gene_level = Integer.parseInt(values[1]);

					if(expression_value > 1250000 && gene_level==42 ) {return true;}return false;
				}).map(line -> new Tuple2<String,Integer>(line.split(",")[0], 1)).groupBy(0).sum(1);
		
        DataSet<Tuple2<String, Integer>> join_result =	disease_extract
			.join(active_genes).where(0).equalTo(0).projectFirst(1).projectSecond(1);

		DataSet<Tuple2<String, Integer>> total_result = join_result.map(line -> line).groupBy(0).sum(1).setParallelism(1)
                        .sortPartition(1, Order.DESCENDING);
		
		DataSet<String> result = total_result.map(line -> line.f0+"\t"+line.f1);
		// total_result.first(100).print();
		result.writeAsText("hdfs:///user/xguo8788/flink/"+"q1");
		env.execute();
	}
}
