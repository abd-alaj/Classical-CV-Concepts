function error = SSD_error(p, q)
    error = sum(abs(p - q).^2);
end 
