use std::cmp::min;
use rand::Rng;
use crate::operators::{crossover, mutation};
use crate::utils::Phenotype;
use crate::utils::vec_column;
use crate::utils::genes_to_string;


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

            if index == segments - 1 {
                break;
            }
        }
        byte_slice
    };

    let mut generations: Vec<Vec<(Vec<[u8; 3]>, Phenotype)>> = vec![];

    println!("\nНачальное поколение: ");
    let start_generation = {
        let mut generation = vec![];

        let mut generator_column_of_matrix = {
            let mut columns = vec![];
            for i in 0..matrix[0].len() {
                columns.push(vec_column(matrix, i));
            }
            columns.into_iter().cycle()
        };

        for i in 0..z {
            let mut genotype: Vec<[u8; 3]> = vec![];

            println!("\nОсобь{} Генотип: ", i + 1);
            let column = generator_column_of_matrix.next().unwrap();
            for (row_index, el) in column.iter().enumerate() {
                let (col_index, not_inf_task) = {
                    let mut value = *el;
                    let mut k = if value == u32::MAX { 0 } else { i as usize % matrix[row_index].len() };
                    loop {
                        value = matrix[row_index][k];
                        if value == u32::MAX && k < matrix[row_index].len() {
                            k += 1;
                        } else {
                            break;
                        }
                    }
                    (k, value as u8)
                };
                
                let value = {
                    let range = byte_slices.get(col_index).unwrap();
                    rnd.gen_range(range.0..range.1)
                };
                
                genotype.push([not_inf_task, value, row_index as u8]);
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
        let mut new_generation: Vec<(Vec<[u8; 3]>, Phenotype)> = vec![];
        println!(
            "\n------------- {} №{} -------------",
            format!("\x1b[1;33m{}\x1b[0m", "Формирование нового поколения"),
            gen_counter + 1
        );

        for (i1_index, individual1) in last_generation.iter().enumerate() {

            let (individual2, i2_index) = {
                let mut rnd_individual2 = rnd.gen_range(0..last_generation.len());
                while rnd_individual2 == i1_index {
                    rnd_individual2 = rnd.gen_range(0..last_generation.len());
                }
                (&last_generation[rnd_individual2], rnd_individual2)
            };

            let great_child= {

                println!("\n> - - - - - - - Скрещивание особей {} и {} - - - - - - - <", i1_index + 1, i2_index + 1);
                println!("\nОсобь{} Генотип: ", i1_index + 1);
                println!("{}", genes_to_string(&individual1.0));
                &individual1.1.print();
                println!("Определитель фенотипа: {}", individual1.1.max_sum);


                println!("\nОсобь{} Генотип: ", i2_index + 1);
                println!("{}", genes_to_string(&individual2.0));
                &individual2.1.print();
                println!("Определитель фенотипа: {}", individual2.1.max_sum);

                let mut child1 = individual1.clone();
                let mut child2 = individual2.clone();

                if rnd.gen_range(0..100) < p_k {

                    println!("\nВыполнился оператор кроссовера с вероятностью {}%", p_k);

                    let (new_individual1, new_individual2) = crossover(&individual1.0, &individual2.0);

                    child1.0 = new_individual1;
                    child2.0 = new_individual2;
                    child1.1 = Phenotype::new(&byte_slices, &child1.0);
                    child2.1 = Phenotype::new(&byte_slices, &child2.0);


                    println!("Особь [1] Генотип: ");
                    println!("{}", genes_to_string(&child1.0));
                    child1.1.print();

                    println!("\nОсобь [2] Генотип: ");
                    println!("{}", genes_to_string(&child2.0));
                    child2.1.print();

                }
                if rnd.gen_range(0..100) < p_m {
                    println!("\nВыполнился оператор мутации с вероятностью {}%", p_m);
                    let mut is_mutated = false;
                    for try_attempt in 0..3 {
                        println!("Попытка мутации №{}", try_attempt + 1);
                        let (mut1_new_genes, mut1_logs) = mutation(&child1.0);
                        let (mut2_new_genes, mut2_logs) = mutation(&child2.0);
    
                        let child1_gens = Phenotype::re_genes(&byte_slices, matrix, &mut1_new_genes);
                        let child1_phen = Phenotype::new(&byte_slices, &child1_gens);
    
                        let child2_gens = Phenotype::re_genes(&byte_slices, matrix, &mut2_new_genes);
                        let child2_phen = Phenotype::new(&byte_slices, &child2_gens);
    
                        println!("Особь [1] Генотип: ");
                        println!("{}", genes_to_string(&child1_gens));
                        print!("\n{}\n", mut1_logs.iter().map(|x| format!("{} ", x)).collect::<String>());
                        println!("\nФенотип: ");
                        child1_phen.print();
                        
                        if child1_phen.has_inf() {
                            println!("В результате мутации первого ребенка обнаружена бесконечность");
                            continue;
                        }
    
                        println!("\nОсобь [2] Генотип: ");
                        println!("{}", genes_to_string(&child2_gens));
                        print!("\n{}\n", mut2_logs.iter().map(|x| format!("{} ", x)).collect::<String>());
                        println!("\nФенотип: ");
                        child2_phen.print();
                        
                        if child2_phen.has_inf() {
                            println!("В результате мутации второго ребенка обнаружена бесконечность");
                            continue;
                        }
                        
                        child1.0 = child1_gens;
                        child1.1 = child1_phen;
                        child2.0 = child2_gens;
                        child2.1 = child2_phen;
                        is_mutated = true;
                        break;
                    }
                    
                    if !is_mutated {
                        println!("Мутация не удалась");
                    } else {
                        println!("Мутация прошла успешно");
                    }
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
            if great_child.1.has_inf() {
                panic!("В результате обнаружена бесконечность")
            }
            println!("Определитель фенотипа: {}", great_child.1.max_sum);
            if great_child.1.max_sum < individual1.1.max_sum && great_child.1.max_sum < individual2.1.max_sum {
                println!("Ребенок лучше обоих родителей: {} < {} и {}", great_child.1.max_sum, individual1.1.max_sum, individual2.1.max_sum);
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

    println!("\nВремя выполнения: {:?} мс", delta_time);
    print!("Количество поколений: {}\n", gen_counter + 1);
}