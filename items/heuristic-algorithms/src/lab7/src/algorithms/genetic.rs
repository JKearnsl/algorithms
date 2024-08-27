use std::io::Write;
use rand::Rng;
use rand::seq::SliceRandom;
use crate::utils::{alphabet, crossover, mutation, save_graph_with_path};


fn calc_phenotype(matrix: &Vec<Vec<u32>>, genotype: &Vec<char>) -> (u32, String) {
    let alphas_vec = alphabet().collect::<Vec<char>>()[..matrix.len()].to_vec();
    let alphas_hash: std::collections::HashMap<char, usize> = alphas_vec.iter().enumerate().map(|(i, &x)| (x, i)).collect();
    let pairs = genotype.iter().zip(genotype.iter().skip(1));
    let mut sum = 0;
    let mut log_str = String::new();
    for (a, b) in pairs {
        let val = matrix[alphas_hash[a]][alphas_hash[b]];
        sum += val;
        log_str.push_str(&format!("{:4}", val));
    }
    log_str.push_str(&format!(" = {}\n", sum));
    (sum, log_str)
}

pub fn main(matrix: &Vec<Vec<u32>>, k: u32, z: u32, p_k: u32, p_m: u32, start_vertice: u32) {
    let mut log_file = std::fs::File::create("genetic.log").unwrap();
    let mut rnd = rand::thread_rng();
    let mut generations: Vec<Vec<(Vec<char>, u32)>> = vec![];

    let alphas_vec = alphabet().collect::<Vec<char>>()[..matrix.len()].to_vec();
    let alphas_hash: std::collections::HashMap<char, usize> = alphas_vec.iter().enumerate().map(|(i, &x)| (x, i)).collect();
    let available_genes: Vec<char> = alphas_vec.clone().iter().filter(
        |&x| *x != alphas_vec.get(start_vertice as usize).unwrap().clone()
    ).map(|&x| x).collect();
    let start_alpha = alphas_vec.get(start_vertice as usize).unwrap();
    
    log_file.write("\nНачальное поколение: \n".to_string().as_ref()).expect("Ошибка записи");
    let start_generation = {
        let mut generation = vec![];

        for i in 0..z {
            let mut genotype: Vec<char> = vec![];

            log_file.write(format!("\nОсобь [{}] Генотип: \n", i + 1).as_ref()).expect("Ошибка записи");
            let mut genes = available_genes.clone();
            genes.shuffle(&mut rnd);

            log_file.write(format!("{:4}", start_alpha).as_ref()).expect("Ошибка записи");
            genotype.push(start_alpha.clone());
            for el in genes.iter() {
                log_file.write(format!("{:4}", el).as_ref()).expect("Ошибка записи");
                genotype.push(el.clone());
            }
            log_file.write(format!("{:4}\n", start_alpha).as_ref()).expect("Ошибка записи");
            genotype.push(start_alpha.clone());

            let (max_sum, log_str) = calc_phenotype(matrix, &genotype);
            log_file.write(format!("{}\n", log_str).as_ref()).expect("Ошибка записи");

            generation.push((genotype, max_sum));
        }
        generation
    };
    generations.push(start_generation);

    let start_time = std::time::Instant::now();
    let mut gen_counter = 0;
    loop {
        let last_generation = generations.last().unwrap();
        let mut new_generation: Vec<(Vec<char>, u32)> = vec![];
        log_file.write(format!(
            "\n------------- {} №{} -------------\n",
            "Формирование нового поколения",
            gen_counter + 1
        ).as_ref()).expect("Ошибка записи");

        for (i1_index, individual1) in last_generation.iter().enumerate() {

            let (individual2, i2_index) = {
                let mut rnd_individual2 = rnd.gen_range(0..last_generation.len());
                while rnd_individual2 == i1_index {
                    rnd_individual2 = rnd.gen_range(0..last_generation.len());
                }
                (&last_generation[rnd_individual2], rnd_individual2)
            };

            let great_child= {

                log_file.write(format!(
                    "\n> - - - - - - - Скрещивание особей {} и {} - - - - - - - <\n",
                    i1_index + 1, 
                    i2_index + 1
                ).as_ref()).expect("Ошибка записи");
                log_file.write(format!("\nОсобь [{}] Генотип: \n", i1_index + 1).as_ref()).expect("Ошибка записи");

                for el in individual1.0.iter() {
                    log_file.write(format!("{:4}", el).as_ref()).expect("Ошибка записи");
                }
                log_file.write("\n".to_string().as_ref()).expect("Ошибка записи");
                log_file.write(format!("Фенотип: {}\n", individual1.1).as_ref()).expect("Ошибка записи");

                log_file.write(format!("\nОсобь [{}] Генотип: \n", i2_index + 1).as_ref()).expect("Ошибка записи");

                for el in individual2.0.iter() {
                    log_file.write(format!("{:4}", el).as_ref()).expect("Ошибка записи");
                }
                log_file.write("\n".to_string().as_ref()).expect("Ошибка записи");
                log_file.write(format!("Фенотип: {}\n", individual2.1).as_ref()).expect("Ошибка записи");

                let mut child1 = individual1.clone();
                let mut child2 = individual2.clone();

                if rnd.gen_range(0..100) < p_k {

                    log_file.write(format!("\nВыполнился оператор кроссовера с вероятностью {}%\n", p_k).as_ref()).expect("Ошибка записи");

                    let (geno1, geno2) = crossover(&child1.0, &child2.0);

                    log_file.write(format!("Особь [#1] Генотип: \n").as_ref()).expect("Ошибка записи");
                    for el in geno1.iter() {
                        log_file.write(format!("{:4}", el).as_ref()).expect("Ошибка записи");
                    }
                    log_file.write("\n".to_string().as_ref()).expect("Ошибка записи");

                    let (sum1, log_str1) = calc_phenotype(matrix, &geno1);
                    log_file.write(format!("{}\n", log_str1).as_ref()).expect("Ошибка записи");

                    log_file.write(format!("\nОсобь [#2] Генотип: \n").as_ref()).expect("Ошибка записи");
                    for el in geno2.iter() {
                        log_file.write(format!("{:4}", el).as_ref()).expect("Ошибка записи");
                    }
                    log_file.write("\n".to_string().as_ref()).expect("Ошибка записи");
                    let (sum2, log_str2) = calc_phenotype(matrix, &geno2);
                    log_file.write(format!("{}\n", log_str2).as_ref()).expect("Ошибка записи");
                    
                    child1 = (geno1, sum1);
                    child2 = (geno2, sum2);
                    
                }
                if rnd.gen_range(0..100) < p_m {

                    log_file.write(format!("\nВыполнился оператор мутации с вероятностью {}%\n", p_m).as_ref()).expect("Ошибка записи");

                    let (geno1, log_str1) = mutation(&child1.0);
                    let (geno2, log_str2) = mutation(&child2.0);

                    log_file.write(format!("Особь [1] Генотип: \n").as_ref()).expect("Ошибка записи");
                    for el in geno1.iter() {
                        log_file.write(format!("{:4}", el).as_ref()).expect("Ошибка записи");
                    }
                    log_file.write("\n".to_string().as_ref()).expect("Ошибка записи");
                    log_file.write(format!("{}\n", log_str1).as_ref()).expect("Ошибка записи");

                    let (sum1, log_str1) = calc_phenotype(matrix, &geno1);
                    log_file.write(format!("{}\n", log_str1).as_ref()).expect("Ошибка записи");

                    log_file.write(format!("\nОсобь [2] Генотип: \n").as_ref()).expect("Ошибка записи");
                    for el in geno2.iter() {
                        log_file.write(format!("{:4}", el).as_ref()).expect("Ошибка записи");
                    }
                    log_file.write("\n".to_string().as_ref()).expect("Ошибка записи");
                    log_file.write(format!("{}\n", log_str2).as_ref()).expect("Ошибка записи");
                    let (sum2, log_str2) = calc_phenotype(matrix, &geno2);
                    log_file.write(format!("{}\n", log_str2).as_ref()).expect("Ошибка записи");
                    
                    child1 = (geno1, sum1);
                    child2 = (geno2, sum2);
                    
                }
                
                let local_best_child = {
                    if child1.1 < child2.1 {
                        child1
                    } else {
                        child2
                    }
                };
                
                if individual1.1 < local_best_child.1 {
                    individual1.clone()
                } else { 
                    local_best_child
                }
                
            };
            log_file.write(format!("\nЛучший ребенок: \n").as_ref()).expect("Ошибка записи");
            for el in great_child.0.iter() {
                log_file.write(format!("{:4}", el).as_ref()).expect("Ошибка записи");
            }
            log_file.write("\n".to_string().as_ref()).expect("Ошибка записи");
            log_file.write(format!("Фенотип: {}\n", great_child.1).as_ref()).expect("Ошибка записи");
            
            if great_child.1 < individual1.1 && great_child.1 < individual2.1 {
                log_file.write(format!(
                    "Ребенок лучше обоих родителей: {} < {} и {}\n", 
                    great_child.1, 
                    individual1.1, 
                    individual2.1
                ).as_ref()).expect("Ошибка записи");
            }
            new_generation.push(great_child);
        }

        if generations.len() >= k as usize {
            let mut last_greet: Vec<u32> = vec![];
            for index in (generations.len() - k as usize)..generations.len() {
                let last_gen = &generations[index];
                let min_max_sum = last_gen.iter().min_by_key(|el| el.1).unwrap().1;
                last_greet.push(min_max_sum);
            }
            log_file.write(format!(
                "Последние {} поколений имеют лучший определитель фенотипа {:?} соответственно\n",
                k,
                last_greet
            ).as_ref()).expect("Ошибка записи");
            if last_greet.iter().all(|&x| x == last_greet[0]) {
                log_file.write(format!(
                    "Остановка алгоритма: последние {} поколений имеют одинаковый определитель фенотипа лучшей особи\n",
                    k
                ).as_ref()).expect("Ошибка записи");

                let last_gen = generations.last().unwrap();
                let best_genotype = last_gen.iter().min_by_key(|el| el.1).unwrap().0.clone();
                let (_, best_phenotype) = calc_phenotype(matrix, &best_genotype);
                log_file.write(format!("\nЛучшая особь: \n").as_ref()).expect("Ошибка записи");
                for el in best_genotype.iter() {
                    log_file.write(format!("{:4}", el).as_ref()).expect("Ошибка записи");
                }
                log_file.write("\n".to_string().as_ref()).expect("Ошибка записи");
                log_file.write(format!("{}\n", best_phenotype).as_ref()).expect("Ошибка записи");

                break;
            }
        }

        // new_generation.extend(last_generation.iter().cloned());
        // new_generation.sort_by(|a, b| a.1.cmp(&b.1));
        // new_generation.truncate(z as usize);

        generations.push(new_generation);
        gen_counter += 1;
    }
    let delta_time = start_time.elapsed().as_millis();
    
    log_file.write(format!("\n\nВремя выполнения: {:?} мс", delta_time).as_ref()).expect("Ошибка записи");
    log_file.write(format!("Количество поколений: {}\n", gen_counter + 1).as_ref()).expect("Ошибка записи");

    save_graph_with_path(
        matrix.clone(),
        generations.last().unwrap().iter().min_by_key(|el| el.1).unwrap().0.clone().iter().map(
            |&x| alphas_hash[&x]
        ).collect(),
        "genetic_genetic".to_string()
    );
}

// Мутация на беск и мы присекаем и с одного комп на другой и присек