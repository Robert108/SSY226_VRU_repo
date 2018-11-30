      if ~any(isnan(mag))
      Lm = (1-alpha_m)*Lm_prev + alpha_m*norm(mag); % AR(1) filter
          if  Lm_prev*0.98 < Lm && Lm < Lm_prev*1.02;
              magOut = false;
              Lm_prev = Lm;
          else 
              magOut = true;
          end  
      else
          magOut = false;
      end       
     ownView.setMagDist(magOut);