use std::cmp::Ordering;

#[derive(Clone)]
pub struct Phenotype {
    pub matrix: Vec<Vec<u8>>,
    pub max_sum : u32,
    max_sum_index: usize,
    byte_slices: Vec<(u8, u8)>,
}


impl Phenotype {
    pub fn new(byte_slices: &Vec<(u8, u8)>, genotype: &Vec<[u8; 2]>) -> Phenotype {
        let matrix = {
            let mut buffer_matrix: Vec<Vec<u8>> = vec![vec![]; byte_slices.len()];
            for (i, range) in byte_slices.iter().enumerate() {
                let mut buffer = vec![];
                for gen in genotype.iter() {
                    if range.0 <= gen[1] && gen[1] <= range.1 {
                        buffer.push(gen[0]);
                    }
                }
                buffer_matrix[i] = buffer;
            }
            buffer_matrix
        };

        let max_sum = matrix.iter().map(|row| row.iter().map(|x| *x as u32).sum::<u32>()).max().unwrap();
        let max_sum_index = matrix.iter().position(|row| row.iter().map(|x| *x as u32).sum::<u32>() == max_sum).unwrap();
        Phenotype { matrix, max_sum, max_sum_index, byte_slices: byte_slices.clone()}
    }

    pub fn print(&self) {
        let max_length = self.matrix.iter().map(|row| row.len()).max().unwrap();
        for (i, row) in self.matrix.iter().enumerate() {
            print!("[{}] {:>15}\t", i, format!("[{}...{}]", self.byte_slices[i].0, self.byte_slices[i].1));
            for cell in row.iter() {
                print!("{:<4}", cell);
            }
            let mut count = max_length - row.len();
            while count > 0 {
                print!("    ");
                count -= 1;
            }
            print!("| Сумма: {}", row.iter().map(|x| *x as u32).sum::<u32>());
            if i == self.max_sum_index {
                print!(" <- max");
            }
            println!();
        }
    }
}

impl Eq for Phenotype {}

impl PartialEq<Self> for Phenotype {
    fn eq(&self, other: &Self) -> bool {
        self.matrix == other.matrix
    }
}

impl PartialOrd<Self> for Phenotype {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        Some(self.cmp(other))
    }
}

impl Ord for Phenotype {
    fn cmp(&self, other: &Self) -> Ordering {
        self.matrix.cmp(&other.matrix)
    }
}
