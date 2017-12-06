import java.util.*;

public class Graph<K, V>
{
	
	private Boolean directed;
	private HashMap<K, V> vertices;
	private HashMap<K, LinkedList<Edge<K>>> adj_list;
	
	public Graph(Boolean directed)
	{
		__init__();
		this.directed = directed;
	}
	
	public Graph()
	{
		__init__();
		this.directed = false;
	}
	
	private void __init__()
	{
		this.vertices = new HashMap<K, V>();
		this.adj_list  = new HashMap<K, LinkedList<Edge<K>>>();
	}
	
	protected LinkedList<Edge<K>> get_neighbors(K key)
	{
		if(!vertices.containsKey(key)) throw new IllegalArgumentException(
				"Error: Vertex " + key + " Does Not Exist.");
		
		return this.adj_list.get(key);
	}
	
	public void add_edge(K key1, V vertex1, K key2, V vertex2, double weight)
	{
		if(!this.vertices.containsKey(key1)) add_vertex(key1, vertex1);
		if(!this.vertices.containsKey(key2)) add_vertex(key2, vertex2);
		
		Edge<K> key_1_2 = new Edge<K>(key2, weight);
		this.adj_list.get(key1).add(key_1_2);
		
		if(this.directed == false)
		{
			Edge<K> key_2_1 = new Edge<K>(key1, weight);
			this.adj_list.get(key2).add(key_2_1);			
		}
	}
	
	private void add_vertex(K key, V vertex)
	{
		this.vertices.put(key, vertex);
		LinkedList<Edge<K>> list = new LinkedList<Edge<K>>();
		this.adj_list.put(key, list);
	}
	
	//Depth First Search Variables:
	private HashMap<K, Boolean> dfs_visited;
	private HashMap<K, Integer> dfs_finishTimes;
	private int dfsTime;
	
	public LinkedList<K> topological_sort()
	{
		dfs_visited = new HashMap<K, Boolean>();
		dfs_finishTimes = new HashMap<K, Integer>();
		LinkedList<K> topList = new LinkedList<K>();
		
		for(K key : this.vertices.keySet())
		{
			this.dfs_visited.put(key, false);
			this.dfs_finishTimes.put(key,  -1);
		}
		
		for(K key : this.vertices.keySet())
		{
			if(this.dfs_visited.get(key) == false)
			{
				dfs_visit(topList, key);
			}
		}
		
		return topList;
	}
	
	private void dfs_visit(LinkedList<K> topList, K iKey)
	{
		this.dfs_visited.put(iKey, true);
		
		LinkedList<Edge<K>> neighborEdges = this.adj_list.get(iKey);
		for(Edge<K> edge : neighborEdges)
		{
			K edgeKey = edge.getKey();
			if(this.dfs_visited.get(edgeKey) == false)
			{
				dfs_visit(topList, edgeKey);
			}
		}
		
		this.dfsTime++;
		this.dfs_finishTimes.put(iKey, this.dfsTime);
		//Add this vertex to the FRONT of the list:
		topList.addFirst(iKey);	
		
	}
	
	public void print_graph()
	{
		for(K key: vertices.keySet())
		{
			System.out.println(key + ":  ");
			List<Edge<K>> edgeList = this.adj_list.get(key);
			for(Edge<K> e : edgeList)
			{
				System.out.println("\t" + e.getKey() + ", " + e.getWeight());
			}
			System.out.println("");
		}
	}
	
	//__________________________________________________
	//* * * * SHORTEST PATH PROPERTIES * * * * *
	HashMap<K, Double> distanceTable;
	HashMap<K, K> predecessorTable;
	
	private class EdgeComparator implements Comparator <Edge<K>> 
	{
		public int compare(Edge<K> o1, Edge<K> o2) 
		{
			return (o1.getWeight() < o2.getWeight()) ? 0 : 1;
		}	
	}
	
	public Stack<K> shortestPath(K from, K to)
	{
		Comparator<Edge<K>> comp = new EdgeComparator();
		
		//Build distance & predecessor tables:
		dijkstra_sp(from, comp);
		
		Stack<K> path = new Stack<K>();
		K previous = to;
		while(previous != from && previous != null)
		{
			path.push(previous);
			previous = predecessorTable.get(previous);
		}
		if(previous == null) return null;
		path.push(previous);
		return path;
	}
	
	private void dijkstra_sp(K from, Comparator<Edge<K>> comp)
	{
		
		distanceTable = new HashMap<K, Double>();
		predecessorTable = new HashMap<K, K>();
		HashMap<K, Boolean> visited = new HashMap<K, Boolean>();
		
		//Initialize Queue that keeps "light edge" at head 
		PriorityQueue<Edge<K>> queue = new PriorityQueue<Edge<K>>(comp);
		Edge<K> source_edge = new Edge<K>(from, 0);
		queue.add(source_edge);
		
		for(K key : this.vertices.keySet())
		{
			distanceTable.put(key, Double.MAX_VALUE);
			predecessorTable.put(key, null);
			visited.put(key, false);
		}
	
		visited.put(from, true);
		distanceTable.put(from, (double)0);
		
		while(queue.isEmpty() == false)
		{
			K onKey = queue.poll().getKey();
			double onDistance = distanceTable.get(onKey);
					
			LinkedList<Edge<K>> neighborEdges = adj_list.get(onKey);
			
			for(Edge<K> edge : neighborEdges)
			{
				//Check if neighbor just found a shorter path:
				K neighborKey = edge.getKey();
				if(distanceTable.get(neighborKey) > (onDistance + edge.getWeight()))
				{
					predecessorTable.put(neighborKey, onKey);
					distanceTable.put(neighborKey, onDistance + edge.getWeight());		
				}
				
				if(visited.containsKey(neighborKey) == false) queue.add(edge);
				
			}	
		}
	}//End Dijkstra (Build distance & predecessor tables)
	
	
}
