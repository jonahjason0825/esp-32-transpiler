Welcome to the readme of the ".easy" files for ESP32!
This is the brainchild of my need for an alternative to the testing syntax of ESP-IDF. 
I hope you enjoy using it as much as I enjoyed coding it for you!

How to use
This is not intended to be another technical sheet. I aim to involve students who are new to ESP-IDF and intend to bridge the gap between programming and learning new syntax.

All files are saved in a .easy extension. The compiler.py file does the heavy lifting, as the below ESP-IDF commands are coded into it.
The output ESP-IDF code is saved to main/main.c. You may copy-paste the generated code into your IDE of choice for programming ESP32.
Please exclusively use the below-mentioned syntax AS-IS. Do not change spellings or case. 

Syntax:
1. setPin pin_number: setting a pin to HIGH or LOW state.
2. 
ESP-IDF syntax: 
	gpio_reset_pin({pin_number}); 
    gpio_set_direction({pin_number}, GPIO_MODE_OUTPUT); 
    gpio_set_level({pin_number}, {1 if pin_state in ('HIGH', '1') else 0});
	
3. readPin pin_number: performs digital read on a pin
   
ESP-IDF syntax:
	gpio_get_level({pin_number});

4. holdFor: delay function
ESP-IDF syntax: vTaskDelay(pdMS_TO_TICKS({ms}));


5. getTime: retrieves the time elapsed since ESP32 was booted. 
ESP-IDF syntax: esp_timer_get_time()


6. blinkBuiltIn: blinks the built-in LED on the ESP32, which is generally controlled by GPIO12
ESP-IDF syntax: 
	gpio_reset_pin(12);"
    gpio_set_direction(12, GPIO_MODE_OUTPUT);
    gpio_set_level(12, 1);


7. returnAvailableDRAM: retrieves the amount of DRAM available in ESP32
ESP-IDF syntax:
	printf(\"Available DRAM: %d bytes\\n\", esp_get_free_heap_size());


8. resetChip: performs a software reset on ESP32
ESP-IDF syntax:
	esp_restart();
