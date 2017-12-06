
//K represents the vertex key Type
public class Edge<K> 
{
	private K key;
	private double weight;
	
	public Edge(K key, double weight)
	{
		this.key = key;
		this.weight = weight;
	}
	
	public K getKey() { return key; }
	
	public double getWeight() { return weight; }
	
}
