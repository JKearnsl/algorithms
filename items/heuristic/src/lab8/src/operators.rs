use std::fmt::format;
use rand::Rng;


/**
    Функция, выполняющая операцию скрещивания двух генотипов.
    Он меняет местами фрагменты генотипов из случайных индексов.
    # Arguments
    * `genotype1` - первый генотип
    * `genotype2` - второй генотип
    # Returns
    Кортеж двух генотипов после операции скрещивания.
 */
pub fn crossover(genotype1: &Vec<[u8; 3]>, genotype2: &Vec<[u8; 3]>) -> (Vec<[u8; 3]>, Vec<[u8; 3]>) {
    let mut rnd = rand::thread_rng();
    let mut result1: Vec<[u8; 3]> = vec![];
    let mut result2: Vec<[u8; 3]> = vec![];
    let random_index = rnd.gen_range(0..genotype1.len());

    for (index, (gen1, gen2)) in genotype1.iter().zip(genotype2.iter()).enumerate(){
        if index >= random_index {
            result1.push(*gen2);
            result2.push(*gen1);
        } else {
            result1.push(*gen1);
            result2.push(*gen2);
        }
    }
    (result1, result2)
}


fn highlight_bits(number: u32, bits_to_highlight: &[usize]) -> String {
    let binary_str = format!("{:08b}", number);
    let highlighted_str = binary_str
        .chars()
        .enumerate()
        .map(|(index, bit)| {
            if bits_to_highlight.contains(&index) {
                format!("\x1b[1;31m{}\x1b[0m", bit) // выделяем бит красным цветом
            } else {
                bit.to_string()
            }
        })
        .collect::<String>();
    highlighted_str
}


/**
    Функция, выполняющая операцию мутации генотипа.
    Он меняет местами два случайных бита в случайном гене.
    # Arguments
    * `genotype` - генотип
    # Returns
    Генотип после операции мутации.
 */
pub fn mutation(genotype: &Vec<[u8; 3]>) -> (Vec<[u8; 3]>, Vec<String>) {
    let mut log = vec![];
    let mut rnd = rand::thread_rng();
    let mut new_genotype: Vec<[u8; 3]> = genotype.clone();
    let random_gen_index = rnd.gen_range(0..new_genotype.len());
    let random_bit_1 = rnd.gen_range(0..7);
    let random_bit_2 = loop {
        let value = rnd.gen_range(0..7);
        if value != random_bit_1 {
            break value;
        }
    };

    let mut_gen = genotype[random_gen_index].clone();
    let binary_str = format!("{:08b}", mut_gen[1]);
    let mut binary_str = binary_str.chars().collect::<Vec<char>>();


    let temp = binary_str[random_bit_1];
    binary_str[random_bit_1] = binary_str[random_bit_2];
    binary_str[random_bit_2] = temp;

    let new_byte = u8::from_str_radix(&binary_str.iter().collect::<String>(), 2).unwrap();
    new_genotype[random_gen_index][1] = new_byte;


    log.push(format!(
        "[{}] -> {} -> {} -> [{}]",
        mut_gen[1],
        highlight_bits(mut_gen[1] as u32, &[random_bit_1, random_bit_2]),
        highlight_bits(new_byte as u32, &[random_bit_2, random_bit_1]),
        new_byte
    ));
    (new_genotype, log)
}
