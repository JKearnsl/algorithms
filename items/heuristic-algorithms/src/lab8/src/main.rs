use std::io;
use std::io::Write;

use rand::Rng;

pub mod algorithm;
mod operators;
mod utils;

fn main() {
    let devices = {
        loop {
            print!("Введите количество устройств: ");
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
    let tasks = {
        loop {
            print!("Введите количество задач: ");
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
    let k = {
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
    let z = {
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
        let mut rng = rand::thread_rng();
        let column = {
            let mut column = vec![0; tasks as usize];
            for cell in column.iter_mut() {
                *cell = rng.gen_range(range.0..range.1);
            }
            column
        };
        let mut temp_matrix = vec![vec![0; devices as usize]; tasks as usize];
        for (i, row) in temp_matrix.iter_mut().enumerate() {
            let inf_indexes = loop {
                let values = utils::random_subset(0..tasks as usize);
                if values.len() < devices as usize {
                    break values;
                }
            };
            for (index, cell) in row.iter_mut().enumerate() {
                if inf_indexes.contains(&index) {
                    *cell = u32::MAX;
                    continue
                }
                *cell = column[i];
            }
        }
        temp_matrix
    };

    println!("\nМатрица:");
    for row in matrix.iter() {
        for cell in row.iter() {
            if *cell == u32::MAX {
                print!("{:<4}", "inf");
                continue;
            }
            print!("{:<4}", cell);
        }
        println!();
    }

    loop {
        println!("\nЧто будем делать?: ");
        println!("\t1. Запуск алгоритма");
        println!("\t2. Выход");
        print!("Ваш выбор: ");
        io::stdout().flush().unwrap();
        let mut input = String::new();
        io::stdin().read_line(&mut input).unwrap();
        match input.trim().parse::<u32>() {
            Ok(n) => {
                match n {
                    1 => {
                        algorithm::main(&matrix, k, z, p_k, p_m)
                    }
                    2 => {
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
