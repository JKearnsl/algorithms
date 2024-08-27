use std::io::Write;
use petgraph::Graph;
use rand::Rng;
use crate::utils;

pub fn alphabet() -> impl Iterator<Item = char> {
    (b'a'..=b'z').map(|c| c as char)
}


pub fn crossover(parent1: &Vec<char>, parent2: &Vec<char>) -> (Vec<char>, Vec<char>) {
    let mut rnd = rand::thread_rng();
    let mut child1 = vec![];
    let mut child2 = vec![];

    let cut_point = rnd.gen_range(1..parent1.len() - 2);
    for i in 0..parent1.len() {
        if i < cut_point {
            child1.push(parent1[i]);
            child2.push(parent2[i]);
        } else {
            if i == parent1.len() - 1 {
                child1.push(parent1[i]);
                child2.push(parent2[i]);
                continue;
            }

            if child1.contains(&parent2[i]) {
                let mut j = 0;
                while child1.contains(&parent2[j]) {
                    j += 1;
                }
                child1.push(parent2[j]);
            } else {
                child1.push(parent2[i]);
            }

            if child2.contains(&parent1[i]) {
                let mut j = 0;
                while child2.contains(&parent1[j]) {
                    j += 1;
                }
                child2.push(parent1[j]);
            } else {
                child2.push(parent1[i]);
            }
        }
    }
    (child1, child2)
}

pub fn mutation(genotype: &Vec<char>) -> (Vec<char>, String) {
    let mut rnd = rand::thread_rng();
    let mut indexes = vec![];
    for _ in 0..2 {
        loop {
            let index = rnd.gen_range(1..genotype.len() - 1);
            if !indexes.contains(&index) {
                indexes.push(index);
                break;
            }
        }
    }
    let mut clone_genotype = genotype.clone();
    clone_genotype.swap(indexes[0], indexes[1]);
    
    (clone_genotype, format!("Мутация: {} <-> {}", indexes[0], indexes[1]))
}


pub fn save_start_graph(matrix: Vec<Vec<u32>>) {
    let mut graph: Graph<String, u32, petgraph::Undirected> = Graph::new_undirected();

    let mut alphas = utils::alphabet();
    for i in 0..matrix.len() {
        graph.add_node(format!("{}", alphas.next().unwrap()));
    }
    for i in 0..matrix.len() {
        for j in (i + 1)..matrix.len() {
            graph.add_edge(
                petgraph::graph::NodeIndex::new(i),
                petgraph::graph::NodeIndex::new(j),
                matrix[i][j],
            );
        }
    }

    let dot = petgraph::dot::Dot::new(&graph);
    let dot_str = format!("{:?}", dot);

    let mut file = std::fs::File::create("start_graph.dot").unwrap();
    file.write_all(dot_str.as_bytes()).unwrap();

}


pub fn save_graph_with_path(matrix: Vec<Vec<u32>>, path: Vec<usize>, filename: String) {
    let mut graph: Graph<String, String, petgraph::Undirected> = Graph::new_undirected();

    let mut alphas = alphabet();
    for _ in 0..matrix.len() {
        graph.add_node(format!("{}", alphas.next().unwrap()));
    }
    
    let pairs_path = path.iter().zip(path.iter().skip(1));
    
    for (i, j) in pairs_path {
        graph.add_edge(
            petgraph::graph::NodeIndex::new(*i),
            petgraph::graph::NodeIndex::new(*j),
            format!("{}", matrix[*i][*j]),
        );
    }

    // for i in 0..matrix.len() {
    //     for j in (i + 1)..matrix.len() {
    //         if pairs.clone().any(|(a, b)| *a == i && *b == j) {
    //             graph.add_edge(
    //                 petgraph::graph::NodeIndex::new(i),
    //                 petgraph::graph::NodeIndex::new(j),
    //                 format!("{}", matrix[i][j])
    //             );
    //         } else {
    //             graph.add_edge(
    //                 petgraph::graph::NodeIndex::new(i),
    //                 petgraph::graph::NodeIndex::new(j),
    //                 "".to_string(),
    //             );
    //         }
    //     }
    // }
    
    let dot = petgraph::dot::Dot::new(&graph);
    let dot_str = format!("{:?}", dot);

    let mut file = std::fs::File::create(format!("{}.dot", filename)).unwrap();
    file.write_all(dot_str.as_bytes()).unwrap();
}
