use std::cmp::min;
use rand::Rng;
use crate::operators::{crossover, mutation};
use crate::utils::Phenotype;

fn vec_column<T: Copy>(matrix: &Vec<Vec<T>>, column: usize) -> Vec<T> {
    matrix.iter().map(|row| row[column]).collect()
}

fn genes_to_string(genes: &Vec<[u8; 2]>) -> String {
    let mut first_row = String::new();
    let mut second_row = String::new();
    let mut third_row = String::new();
    for gene in genes.iter() {
        first_row.push_str(&format!("{:^4}", gene[0]));
        second_row.push_str(&format!("{:^4}", "|"));
        third_row.push_str(&format!("{:^4}", gene[1]));
    }
    format!("{}\n{}\n{}", first_row, second_row, third_row)
}


pub fn main(matrix: &Vec<Vec<u32>>, k: u32, z: u32, p_k: u32, p_m: u32) {
    let mut rnd = rand::thread_rng();

    let byte_slices = {
        let start: u8 = 0;
        let end: u8 = 255;
        let segments = matrix[0].len();
        let step = ((end as usize - start as usize) / segments) as u8;

        let mut byte_slice: Vec<(u8, u8)> = vec![];

        println!("\nСегменты байта:");
        let mut segment_start = 0;
        let mut segment_end = 0;

        for (index, value) in (start..end).step_by(step as usize).enumerate() {
            segment_start = min(value, end);
            if index == segments - 1{
                segment_end = end;
            } else {
                segment_end = min(value + step - 1, end);
            }

            byte_slice.push((segment_start, segment_end));
            println!("Сегмент: [{}] {} - {}", value, segment_start, segment_end);

            // bugfix
            if index == segments - 1 {
                break;
            }

        }
        byte_slice
    };

    let mut generations: Vec<Vec<(Vec<[u8; 2]>, Phenotype)>> = vec![];

    println!("\nНачальное поколение: ");
    let start_generation = {
        let mut generation = vec![];
        for i in 0..z {
            let mut genotype: Vec<[u8; 2]> = vec![];

            println!("\nОсобь{} Генотип: ", i + 1);
            let column = vec_column(matrix, 0);
            for el in column.iter() {
                genotype.push([*el as u8, rnd.gen_range(0..255)]);
            }
            println!("{}", genes_to_string(&genotype));

            print!("\nФенотип: \n");
            let phenotype = Phenotype::new(&byte_slices, &genotype);
            phenotype.print();

            generation.push((
                genotype,
                phenotype
            ));
        }
        generation
    };
    generations.push(start_generation);

    let start_time = std::time::Instant::now();
    let mut gen_counter = 0;
    loop {
        let last_generation = generations.last().unwrap();
        let mut new_generation: Vec<(Vec<[u8; 2]>, Phenotype)> = vec![];
        println!("\n------------- Формирование нового поколения №{} -------------", gen_counter + 1);

        for (g1_index, genotype1) in last_generation.iter().enumerate() {

            let (genotype2, g2_index) = {
                let mut rnd_genotype2 = rnd.gen_range(0..last_generation.len());
                while rnd_genotype2 == g1_index {
                    rnd_genotype2 = rnd.gen_range(0..last_generation.len());
                }
                (&last_generation[rnd_genotype2], rnd_genotype2)
            };

            let great_child= {

                println!("\n> - - - - - - -Скрещивание особей {} и {}", g1_index + 1, g2_index + 1);
                println!("\nОсобь{} Генотип: ", g1_index + 1);
                println!("{}", genes_to_string(&genotype1.0));
                println!("Определитель фенотипа: {}", genotype1.1.max_sum);


                println!("\nОсобь{} Генотип: ", g2_index + 1);
                println!("{}", genes_to_string(&genotype2.0));
                println!("Определитель фенотипа: {}", genotype2.1.max_sum);

                let mut child1 = genotype1.clone();
                let mut child2 = genotype2.clone();

                if rnd.gen_range(0..100) < p_k {

                    println!("\nВыполнился оператор кроссовера с вероятностью {}%", p_k);

                    let (new_genotype1, new_genotype2) = crossover(&genotype1.0, &genotype2.0);
                    child1.0 = new_genotype1;
                    child2.0 = new_genotype2;
                    child1.1 = Phenotype::new(&byte_slices, &child1.0);
                    child2.1 = Phenotype::new(&byte_slices, &child2.0);

                    println!("Особь [1] Генотип: ");
                    println!("{}", genes_to_string(&child1.0));

                    println!("\nОсобь [2] Генотип: ");
                    println!("{}", genes_to_string(&child2.0));

                }
                if rnd.gen_range(0..100) < p_m {

                    println!("\nВыполнился оператор мутации с вероятностью {}%", p_m);

                    child1.0 = mutation(&child1.0);
                    child2.0 = mutation(&child2.0);
                    child1.1 = Phenotype::new(&byte_slices, &child1.0);
                    child2.1 = Phenotype::new(&byte_slices, &child2.0);

                    println!("Особь [1] Генотип: ");
                    println!("{}", genes_to_string(&child1.0));
                    println!("\nФенотип: ");
                    child1.1.print();

                    println!("\nОсобь [2] Генотип: ");
                    println!("{}", genes_to_string(&child2.0));
                    println!("\nФенотип: ");
                    child2.1.print();
                }

                if child1.1.max_sum < child2.1.max_sum {
                    child1
                } else {
                    child2
                }
            };
            println!("\nЛучший ребенок: ");
            println!("Генотип: ");
            println!("{}", genes_to_string(&great_child.0));
            println!("\nФенотип: ");
            great_child.1.print();
            println!("Определитель фенотипа: {}", great_child.1.max_sum);
            if great_child.1.max_sum < genotype1.1.max_sum && great_child.1.max_sum < genotype2.1.max_sum {
                println!("Ребенок лучше обоих родителей: {} < {} и {}", great_child.1.max_sum, genotype1.1.max_sum, genotype2.1.max_sum);
            }
            new_generation.push(great_child);
        }

        if generations.len() >= k as usize {
            let mut last_greet: Vec<u32> = vec![];
            for index in (generations.len() - k as usize)..generations.len() {
                let last_gen = &generations[index];
                let min_max_sum = last_gen.iter().map(|el| el.1.max_sum).min().unwrap();
                last_greet.push(min_max_sum);
            }
            println!(
                "Последние {} поколений имеют лучший определитель фенотипа {:?} соответственно",
                k,
                last_greet
            );
            if last_greet.iter().all(|&x| x == last_greet[0]) {
                println!("Остановка алгоритма: последние {} поколений имеют одинаковый определитель фенотипа лучшей особи", k);
                break;
            }
        }
        generations.push(new_generation);
        gen_counter += 1;
    }
    let delta_time = start_time.elapsed().as_millis();

    println!("\n--------------- Последнее поколение ---------------");
    for (index, generation) in generations.last().unwrap().iter().enumerate() {
        println!("\nОсобь{}: ", index + 1);
        println!("\nГенотип: ");
        println!("{}", genes_to_string(&generation.0));

        print!("\nФенотип: \n");
        generation.1.print();
    };

    println!("\nВремя выполнения: {:?} мс", delta_time);
    print!("Количество поколений: {}\n", gen_counter + 1);
}