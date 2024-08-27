use std::io;
use std::io::Write;

use rand::Rng;

mod utils;
mod algorithms;



fn main() {

    let vertices = {
        loop {
            print!("Введите количество вершин: ");
            io::stdout().flush().unwrap();
            let mut input = String::new();
            match io::stdin().read_line(&mut input) {
                Ok(_) => (),
                Err(_) => {
                    println!("Некорректный ввод. Попробуйте еще раз.");
                    continue;
                }
            }
            match input.trim().parse::<u32>() {
                Ok(n) => break n,
                Err(_) => {
                    println!("Некорректный ввод. Попробуйте еще раз.");
                    continue;
                }
            }
        }
    };
    let start_vertice = {
        loop {
            print!("Введите начальную вершину: ");
            io::stdout().flush().unwrap();
            let mut input = String::new();
            match io::stdin().read_line(&mut input) {
                Ok(_) => (),
                Err(_) => {
                    println!("Некорректный ввод. Попробуйте еще раз.");
                    continue;
                }
            }
            match input.trim().parse::<u32>() {
                Ok(n) => {
                    if n == 0 || n > vertices {
                        println!("Некорректный ввод. Попробуйте еще раз.");
                        continue;
                    }
                    break n - 1;
                },
                Err(_) => {
                    println!("Некорректный ввод. Попробуйте еще раз.");
                    continue;
                }
            }
        }
    };
    let range: (u32, u32) = {
        loop {
            print!("Введите диапазон значений через запятую: ");
            io::stdout().flush().unwrap();
            let mut input = String::new();
            match io::stdin().read_line(&mut input) {
                Ok(_) => (),
                Err(_) => {
                    println!("Некорректный ввод. Попробуйте еще раз.");
                    continue;
                }
            }

            let trimmed_input = input.trim().replace(" ", "");
            let values: Vec<&str> = trimmed_input.split(',').collect();
            if values.len() != 2 {
                println!("Некорректный ввод. Попробуйте еще раз.");
                continue;
            }
            match (values[0].parse::<u32>(), values[1].parse::<u32>()) {
                (Ok(a), Ok(b)) => break (a, b),
                _ => {
                    println!("Некорректный ввод. Попробуйте еще раз.");
                    continue;
                }
            }
        }
    };
    let mut k = {
        loop {
            print!("Введите количество повторов k: ");
            io::stdout().flush().unwrap();
            let mut input = String::new();
            match io::stdin().read_line(&mut input) {
                Ok(_) => (),
                Err(_) => {
                    println!("Некорректный ввод. Попробуйте еще раз.");
                    continue;
                }
            };
            match input.trim().parse::<u32>() {
                Ok(n) => break n,
                Err(_) => {
                    println!("Некорректный ввод. Попробуйте еще раз.");
                    continue;
                }
            }
        }
    };
    let mut z = {
        loop {
            print!("Введите количество особей в поколении z: ");
            io::stdout().flush().unwrap();
            let mut input = String::new();
            match io::stdin().read_line(&mut input) {
                Ok(_) => (),
                Err(_) => {
                    println!("Некорректный ввод. Попробуйте еще раз.");
                    continue;
                }
            };
            match input.trim().parse::<u32>() {
                Ok(n) => break n,
                Err(_) => {
                    println!("Некорректный ввод. Попробуйте еще раз.");
                    continue;
                }
            }
        }
    };

    let p_k = {
        loop {
            print!("Введите вероятность кроссовера Pk: ");
            io::stdout().flush().unwrap();
            let mut input = String::new();
            match io::stdin().read_line(&mut input) {
                Ok(_) => (),
                Err(_) => {
                    println!("Некорректный ввод. Попробуйте еще раз.");
                    continue;
                }
            };
            match input.trim().parse::<u32>() {
                Ok(n) => {
                    if n > 100 {
                        println!("Значение должно быть от 0 до 100. Попробуйте еще раз.");
                        continue;
                    }
                    break n;
                },
                Err(_) => {
                    println!("Некорректный ввод. Попробуйте еще раз.");
                    continue;
                }
            }
        }
    };
    let p_m = {
        loop {
            print!("Введите вероятность мутации Pm: ");
            io::stdout().flush().unwrap();
            let mut input = String::new();
            match io::stdin().read_line(&mut input) {
                Ok(_) => (),
                Err(_) => {
                    println!("Некорректный ввод. Попробуйте еще раз.");
                    continue;
                }
            };
            match input.trim().parse::<u32>() {
                Ok(n) => {
                    if n > 100 {
                        println!("Значение должно быть от 0 до 100. Попробуйте еще раз.");
                        continue;
                    }
                    break n;
                },
                Err(_) => {
                    println!("Некорректный ввод. Попробуйте еще раз.");
                    continue;
                }
            }
        }
    };

    let matrix = {
        let mut matrix = vec![vec![0; vertices as usize]; vertices as usize];
        let rnd = &mut rand::thread_rng();

        for i in 0..vertices {
            for j in 0..vertices {
                if i == j {
                    continue;
                }
                if matrix[i as usize][j as usize] == 0 {
                    let weight = rnd.gen_range(range.0..range.1);
                    matrix[i as usize][j as usize] = weight;
                    matrix[j as usize][i as usize] = weight;
                }
            }
        }
        matrix
    };

    println!("Матрица смежности: ");
    let mut alphas = utils::alphabet();
    print!("    ");
    for _ in 0..vertices {
        print!("{:>4}", alphas.next().unwrap());
    }
    println!();
    for _ in 0..vertices + 1 {
        print!("----");
    }
    println!();
    alphas = utils::alphabet();
    for row in matrix.iter() {
        print!("{:^3}|", alphas.next().unwrap());
        for cell in row.iter() {
            if *cell == 0 {
                print!("   ■");
            } else {
                print!("{:>4}", cell);
            }
        }
        println!();
    }

    utils::save_start_graph(matrix.clone());
    println!("Граф сохранен в файл start_graph.dot");
    loop {
        println!("\nВыберите тип алгоритма: ");
        println!("\t1. Генетический алгоритм");
        println!("\t2. Жадный алгоритм");
        println!("\t3. Изменить показатели");
        println!("\t4. Выход");
        print!("Ваш выбор: ");
        io::stdout().flush().unwrap();
        let mut input = String::new();
        io::stdin().read_line(&mut input).unwrap();
        match input.trim().parse::<u32>() {
            Ok(n) => {
                match n {
                    1 => {
                        algorithms::genetic::main(&matrix, k, z, p_k, p_m, start_vertice);
                    }
                    2 => {
                        algorithms::greedy::main(&matrix, start_vertice);
                    }
                    3 => {
                        k = {
                            loop {
                                print!("Введите количество повторов k: ");
                                io::stdout().flush().unwrap();
                                let mut input = String::new();
                                match io::stdin().read_line(&mut input) {
                                    Ok(_) => (),
                                    Err(_) => {
                                        println!("Некорректный ввод. Попробуйте еще раз.");
                                        continue;
                                    }
                                };
                                match input.trim().parse::<u32>() {
                                    Ok(n) => break n,
                                    Err(_) => {
                                        println!("Некорректный ввод. Попробуйте еще раз.");
                                        continue;
                                    }
                                }
                            }
                        };
                        z = {
                            loop {
                                print!("Введите количество особей в поколении z: ");
                                io::stdout().flush().unwrap();
                                let mut input = String::new();
                                match io::stdin().read_line(&mut input) {
                                    Ok(_) => (),
                                    Err(_) => {
                                        println!("Некорректный ввод. Попробуйте еще раз.");
                                        continue;
                                    }
                                };
                                match input.trim().parse::<u32>() {
                                    Ok(n) => break n,
                                    Err(_) => {
                                        println!("Некорректный ввод. Попробуйте еще раз.");
                                        continue;
                                    }
                                }
                            }
                        };
                    }
                    4 => {
                        println!("Выход...");
                        break;
                    }
                    _ => {
                        println!("Некорректный ввод. Попробуйте еще раз.");
                        continue;
                    }
                }
                continue;
            }
            Err(_) => {
                println!("Некорректный ввод. Попробуйте еще раз.");
                continue;
            }
        }
    }
}