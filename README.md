# Cache Memory Simulator

This repository contains a **cache memory simulator** implemented in Python. The simulator supports different cache mapping strategies, including:

- **Direct-mapped cache**
- **Set-associative cache**
- **Fully associative cache**

## Usage

The program is named `simulador.py` and expects the following arguments in order:

```sh
python simulador.py <total_cache_size> <line_size> <group_size> <input_file>
```

### Arguments:
1. **Total cache size (bytes):** The total capacity of the cache. Example: `4096` for a 4KB cache.
2. **Line size (bytes):** The size of each cache line. Example: `1024` for a 1KB line.
3. **Group size (units):** The number of lines per group. Example:
   - `1` → Direct-mapped cache
   - Greater than `1` → Set-associative cache
   - Equal to the number of lines → Fully associative cache
4. **Input file:** A file containing a list of memory block accesses in hexadecimal.

## Example

```sh
python simulador.py 4096 1024 1 input.txt
```

This command runs the simulator with a **4KB cache**, **1KB line size**, and **direct mapping** (1 line per group), using `input.txt` as the list of memory accesses.



